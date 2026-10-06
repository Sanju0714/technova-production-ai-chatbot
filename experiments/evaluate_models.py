import os

from dotenv import load_dotenv
from langsmith import Client
from langchain_openai import ChatOpenAI


# ============================================================
# Configuration
# ============================================================

load_dotenv()

DATASET_NAME = "technova-customer-support-eval"

PRIMARY_MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"
SECONDARY_MODEL = "nvidia/nemotron-3-super-120b-a12b"

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

client = Client()


# ============================================================
# Create NVIDIA LLM
# ============================================================

def create_llm(model_name):

    return ChatOpenAI(
        model=model_name,
        base_url=NVIDIA_BASE_URL,
        api_key=os.getenv("NVIDIA_API_KEY"),
        temperature=0,
        max_tokens=256,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        }
    )


# ============================================================
# TechNova knowledge used by the evaluation target
# ============================================================

SYSTEM_PROMPT = """
You are the TechNova customer support assistant.

TechNova is an electronics store.

Orders:

TN1001:
Item: Laptop Pro 14
Status: Shipped
ETA: 2 days

TN1002:
Item: Noise-cancel Earbuds
Status: Processing
ETA: 5 days

TN1003:
Item: Phone X
Status: Delivered
ETA: -

Policies:

Returns:
Returns are accepted within 30 days in the original packaging.

Warranty:
Electronics come with a 1-year manufacturer warranty.

Shipping:
Free shipping is available for orders above Rs.999.
Standard delivery takes 3-5 days.

Never invent information.

Answer the customer's question concisely.
"""


# ============================================================
# Evaluation target
# ============================================================

def create_target(model_name):

    llm = create_llm(model_name)

    def target(inputs):

        question = inputs["question"]

        response = llm.invoke([
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ])

        return {
            "answer": response.content
        }

    return target


# ============================================================
# LLM-as-Judge
# ============================================================

judge_llm = create_llm(PRIMARY_MODEL)


def correctness_evaluator(run, example):

    question = example.inputs["question"]

    reference_answer = example.outputs["reference_answer"]

    generated_answer = run.outputs["answer"]

    prompt = f"""
You are an evaluation judge for a customer-support chatbot.

Evaluate whether the chatbot answer correctly answers the question.

Question:
{question}

Reference answer:
{reference_answer}

Chatbot answer:
{generated_answer}

Scoring rules:

1 = Correct
- The answer is factually correct.
- It answers the question.
- Minor wording differences are acceptable.

0 = Incorrect
- The answer contains incorrect information.
- The answer misses important required information.
- The answer contradicts the reference answer.

Return ONLY one number:

1

or

0
"""

    response = judge_llm.invoke(prompt)

    result = response.content.strip()

    score = 1 if result.startswith("1") else 0

    return {
        "key": "correctness",
        "score": score,
        "comment": (
            "LLM-as-judge evaluation using NVIDIA-hosted "
            "Nemotron 3.5 Lightning."
        )
    }


# ============================================================
# Run LangSmith evaluation
# ============================================================

def run_evaluation(model_name):

    print("\n" + "=" * 70)
    print(f"LANGSMITH EVALUATION")
    print(f"Model: {model_name}")
    print("=" * 70)

    target = create_target(model_name)

    experiment_name = (
        "technova-eval-30b"
        if "3.5-lightning" in model_name
        else "technova-eval-120b"
    )

    print("\nStarting Client().evaluate()...")
    print(f"Dataset: {DATASET_NAME}")
    print(f"Experiment: {experiment_name}")

    results = client.evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[
            correctness_evaluator
        ],
        experiment_prefix=experiment_name,
        description=(
            f"TechNova customer-support evaluation "
            f"for {model_name}"
        ),
        metadata={
            "model_name": model_name,
            "evaluation_type": "llm_as_judge",
            "dataset": DATASET_NAME
        },
        max_concurrency=1
    )

    # Consume the results so the evaluation completes.
    result_list = list(results)

    print("\nEvaluation completed.")

    return result_list


# ============================================================
# Calculate accuracy from LangSmith evaluation results
# ============================================================

def calculate_accuracy(results):

    scores = []

    for result in results:

        # LangSmith result structure can contain
        # evaluation results under evaluation_results.
        evaluation_results = result.get(
            "evaluation_results",
            {}
        )

        for evaluator_result in evaluation_results.values():

            if isinstance(evaluator_result, dict):

                score = evaluator_result.get("score")

                if score is not None:
                    scores.append(float(score))

    if not scores:
        return None

    return sum(scores) / len(scores)


# ============================================================
# Main
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("TECHNOVA LANGSMITH EVALUATION")
    print("=" * 70)

    print(f"Dataset: {DATASET_NAME}")
    print("Examples: 10")

    # --------------------------------------------------------
    # Evaluate 30B
    # --------------------------------------------------------

    results_30b = run_evaluation(
        PRIMARY_MODEL
    )

    accuracy_30b = calculate_accuracy(
        results_30b
    )

    # --------------------------------------------------------
    # Evaluate 120B
    # --------------------------------------------------------

    results_120b = run_evaluation(
        SECONDARY_MODEL
    )

    accuracy_120b = calculate_accuracy(
        results_120b
    )

    # --------------------------------------------------------
    # Final results
    # --------------------------------------------------------

    print("\n\n")
    print("=" * 70)
    print("FINAL LANGSMITH EVALUATION RESULTS")
    print("=" * 70)

    if accuracy_30b is not None:
        print(
            f"30B Accuracy : "
            f"{accuracy_30b * 100:.2f}%"
        )
    else:
        print("30B Accuracy : Check LangSmith evaluation")

    if accuracy_120b is not None:
        print(
            f"120B Accuracy: "
            f"{accuracy_120b * 100:.2f}%"
        )
    else:
        print("120B Accuracy: Check LangSmith evaluation")

    print("=" * 70)

    print("\nOpen LangSmith and verify:")
    print("1. technova-eval-30b experiment")
    print("2. technova-eval-120b experiment")
    print("3. correctness evaluator")
    print("4. Evaluation comparison")


if __name__ == "__main__":
    main()