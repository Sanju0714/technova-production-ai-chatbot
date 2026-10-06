import os
import pandas as pd

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()


MODEL_NAME = "nvidia/nemotron-3.5-lightning-30b-a3b"

llm = ChatOpenAI(
    model=MODEL_NAME,
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


QUESTIONS = [
    "Where is my order TN1001?",
    "What was the item in that order?",
    "When will it arrive?",
    "What is the return policy?",
    "What is the warranty policy?",
    "What is the shipping policy?",
    "Is shipping free?",
    "How many days do I have to return an item?",
    "Does TechNova provide a manufacturer warranty?",
    "Tell me about TechNova's shipping.",
]


def get_token_usage(response):

    usage = response.usage_metadata

    if usage:
        return {
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0)
        }

    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0
    }


def run_conversation():

    conversation = []

    results = []

    for i, question in enumerate(QUESTIONS, start=1):

        conversation.append(
            HumanMessage(content=question)
        )

        response = llm.invoke(conversation)

        usage = get_token_usage(response)

        conversation.append(
            AIMessage(content=response.content)
        )

        results.append({
            "turn": i,
            "question": question,
            "input_tokens": usage["input_tokens"],
            "output_tokens": usage["output_tokens"],
            "total_tokens": usage["total_tokens"]
        })

        print(f"\nTurn {i}")
        print(f"Question: {question}")
        print(f"Input tokens:  {usage['input_tokens']}")
        print(f"Output tokens: {usage['output_tokens']}")
        print(f"Total tokens:  {usage['total_tokens']}")

    df = pd.DataFrame(results)

    print("\n" + "=" * 60)
    print("10-TURN CONVERSATION TOKEN GROWTH")
    print("=" * 60)

    print(df.to_string(index=False))

    print("\nTotal input tokens:", df["input_tokens"].sum())
    print("Total output tokens:", df["output_tokens"].sum())
    print("Total tokens:", df["total_tokens"].sum())

    print(
        "\nInput-token growth:",
        df.iloc[-1]["input_tokens"] - df.iloc[0]["input_tokens"],
        "tokens"
    )

    df.to_csv(
        "results/token_growth_10_turns.csv",
        index=False
    )

    print("\nResults saved to:")
    print("results/token_growth_10_turns.csv")


if __name__ == "__main__":
    run_conversation()