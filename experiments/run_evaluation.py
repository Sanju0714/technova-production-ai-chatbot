import os

from dotenv import load_dotenv
from langsmith import Client
from langsmith.schemas import Example

from app.graph import graph

load_dotenv()

client = Client()

DATASET_NAME = "TechNova Customer Support Evaluation"


def run_chatbot(inputs: dict) -> dict:
    question = inputs["question"]

    config = {
        "configurable": {
            "thread_id": f"evaluation-{question[:20]}"
        },
        "metadata": {
            "model_name": "nvidia/nemotron-3.5-lightning-30b-a3b",
            "user_id": "evaluation-user",
            "app_version": "1.0.0",
            "session_id": "evaluation-session"
        },
        "tags": [
            "technova-bot",
            "evaluation",
            "nemotron-3.5"
        ]
    }

    result = graph.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config=config
    )

    answer = result["messages"][-1].content

    return {
        "answer": answer
    }


if __name__ == "__main__":

    print("=" * 60)
    print("TECHNOVA LANGSMITH EVALUATION")
    print("=" * 60)

    dataset = list(
        client.list_datasets(dataset_name=DATASET_NAME)
    )[0]

    print(f"Dataset: {dataset.name}")
    print(f"Dataset ID: {dataset.id}")

    examples = list(
        client.list_examples(dataset_id=dataset.id)
    )

    print(f"Examples: {len(examples)}")

    print("\nRunning chatbot evaluation...\n")

    for i, example in enumerate(examples, start=1):

        question = example.inputs["question"]

        print(f"{i}. {question}")

        result = run_chatbot({
            "question": question
        })

        print(f"   Answer: {result['answer']}\n")

    print("=" * 60)
    print("Evaluation run completed.")
    print("=" * 60)