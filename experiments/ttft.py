import os
import time
import pandas as pd

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


MODELS = {
    "Nemotron 3.5 Lightning 30B":
        "nvidia/nemotron-3.5-lightning-30b-a3b",

    "Nemotron 3 Super 120B":
        "nvidia/nemotron-3-super-120b-a12b",
}


QUESTION = "Explain TechNova's return policy in one short sentence."


def measure_ttft(model_label, model_name):

    llm = ChatOpenAI(
        model=model_name,
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

    start_time = time.perf_counter()

    first_token_time = None
    full_response = ""

    for chunk in llm.stream(QUESTION):

        content = chunk.content

        if content:
            if first_token_time is None:
                first_token_time = time.perf_counter()

            full_response += content

    end_time = time.perf_counter()

    ttft = first_token_time - start_time
    total_latency = end_time - start_time

    print(f"\nModel: {model_label}")
    print(f"TTFT: {ttft:.3f}s")
    print(f"Total latency: {total_latency:.3f}s")
    print(f"Response: {full_response}")

    return {
        "model": model_label,
        "ttft_seconds": ttft,
        "total_latency_seconds": total_latency
    }


if __name__ == "__main__":

    results = []

    for model_label, model_name in MODELS.items():

        result = measure_ttft(
            model_label,
            model_name
        )

        results.append(result)

    df = pd.DataFrame(results)

    print("\n" + "=" * 60)
    print("TTFT COMPARISON")
    print("=" * 60)

    print(df.round(3))

    df.to_csv(
        "results/ttft_comparison.csv",
        index=False
    )

    print("\nResults saved to:")
    print("results/ttft_comparison.csv")