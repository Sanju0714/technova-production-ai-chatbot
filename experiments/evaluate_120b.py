import os
import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langsmith import Client

load_dotenv()

DATASET_NAME = "TechNova Customer Support Evaluation"

# ---------------------------------------------------------
# 120B MODEL
# ---------------------------------------------------------
model_llm = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b",
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0,
    max_tokens=256,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    }
)

# ---------------------------------------------------------
# LLM JUDGE
# ---------------------------------------------------------
judge_llm = ChatOpenAI(
    model="nvidia/nemotron-3.5-lightning-30b-a3b",
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0,
    max_tokens=256,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    }
)

JUDGE_PROMPT = """
You are an evaluation judge for a customer-support chatbot.

Compare the chatbot answer against the reference answer.

Return:
- score = 1 if the chatbot answer is factually correct and answers the question.
- score = 0 if it contains an important factual error, contradiction, or fails to answer the question.

Minor differences in wording are acceptable.
Additional correct information is acceptable.
Do not require the answer to use exactly the same wording as the reference.

Return ONLY valid JSON in this format:

{{
  "score": 1,
  "reason": "Brief explanation"
}}

Question:
{question}

Reference answer:
{reference}

Chatbot answer:
{answer}
"""


def generate_answer(question):

    response = model_llm.invoke(question)

    return response.content


def judge_answer(question, reference, answer):

    prompt = JUDGE_PROMPT.format(
        question=question,
        reference=reference,
        answer=answer
    )

    response = judge_llm.invoke(prompt)

    content = response.content.strip()

    try:
        result = json.loads(content)

        score = int(result["score"])
        reason = result["reason"]

        if score not in [0, 1]:
            raise ValueError("Score must be 0 or 1.")

        return score, reason

    except Exception as e:
        print("Judge parsing error:", e)
        print("Raw judge response:", content)

        return 0, "Judge response could not be parsed."


if __name__ == "__main__":

    client = Client()

    datasets = list(
        client.list_datasets(dataset_name=DATASET_NAME)
    )

    if not datasets:
        raise ValueError("Dataset not found.")

    dataset = datasets[0]

    examples = list(
        client.list_examples(dataset_id=dataset.id)
    )

    print("=" * 60)
    print("TECHNOVA 120B MODEL EVALUATION")
    print("=" * 60)

    print(f"Dataset: {dataset.name}")
    print(f"Examples: {len(examples)}")
    print("Model: nvidia/nemotron-3-super-120b-a12b")

    total_score = 0

    for i, example in enumerate(examples, start=1):

        question = example.inputs["question"]
        reference = example.outputs["answer"]

        print(f"\n{i}. {question}")

        answer = generate_answer(question)

        print(f"   Answer: {answer}")

        score, reason = judge_answer(
            question,
            reference,
            answer
        )

        total_score += score

        print(f"   Score: {score}")
        print(f"   Reason: {reason}")

    accuracy = (total_score / len(examples)) * 100

    print("\n" + "=" * 60)
    print("FINAL 120B EVALUATION")
    print("=" * 60)

    print(f"Total questions: {len(examples)}")
    print(f"Correct answers: {total_score}")
    print(f"Accuracy: {accuracy:.2f}%")