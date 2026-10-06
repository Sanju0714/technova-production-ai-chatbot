import os
import time
import pandas as pd

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

MODEL_NAME = "nvidia/nemotron-3-super-120b-a12b"

llm = ChatOpenAI(
    model=MODEL_NAME,
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0,
    max_tokens=128,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    }
)

QUESTIONS = [
    "Where is my order TN1001?",
    "Where is my order TN1002?",
    "Where is my order TN1003?",
    "What is the return policy?",
    "What is the warranty policy?",
    "What is the shipping policy?",
    "How long does standard shipping take?",
    "Is shipping free?",
    "Can I return an electronic product?",
    "How long is the warranty?",
    "What item is in order TN1001?",
    "What item is in order TN1002?",
    "What is the status of order TN1003?",
    "When will order TN1001 arrive?",
    "When will order TN1002 arrive?",
    "Can I get free shipping?",
    "How many days do I have to return an item?",
    "Does TechNova provide a manufacturer warranty?",
    "Tell me about TechNova's shipping.",
    "Tell me about TechNova's return policy.",
]


def run_benchmark():

    results = []

    for i, question in enumerate(QUESTIONS, start=1):

        start_time = time.perf_counter()

        response = llm.invoke(question)

        end_time = time.perf_counter()

        latency = end_time - start_time

        results.append({
            "question": question,
            "latency_seconds": latency,
            "answer": response.content
        })

        print(
            f"{i:02d}. {latency:.2f}s - {question}"
        )

    df = pd.DataFrame(results)

    print("\n--- Latency Results ---")
    print(f"Average: {df['latency_seconds'].mean():.2f}s")
    print(f"P50:     {df['latency_seconds'].quantile(0.50):.2f}s")
    print(f"P95:     {df['latency_seconds'].quantile(0.95):.2f}s")
    print(f"Max:     {df['latency_seconds'].max():.2f}s")

    df.to_csv(
        "results/latency_nemotron120b.csv",
        index=False
    )

    print(
        "\nResults saved to "
        "results/latency_nemotron120b.csv"
    )


if __name__ == "__main__":
    run_benchmark()