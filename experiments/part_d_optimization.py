import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

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
    "What is the return policy?",
    "What is the warranty policy?",
    "What is the shipping policy?",
    "How long does standard shipping take?",
    "Is shipping free?",
    "Can I return an electronic product?",
    "How long is the warranty?",
    "Can I get free shipping?",
    "How many days do I have to return an item?",
    "Does TechNova provide a manufacturer warranty?"
]


def get_tokens(response):
    usage = response.usage_metadata or {}

    return (
        usage.get("input_tokens", 0),
        usage.get("output_tokens", 0),
        usage.get("total_tokens", 0)
    )


def run_full_history():

    history = []
    total_input = 0
    total_output = 0
    total_tokens = 0

    for question in QUESTIONS:

        history.append(
            HumanMessage(content=question)
        )

        response = llm.invoke(history)

        input_tokens, output_tokens, tokens = get_tokens(response)

        total_input += input_tokens
        total_output += output_tokens
        total_tokens += tokens

        history.append(
            AIMessage(content=response.content)
        )

    return total_input, total_output, total_tokens


def run_recent_history():

    history = []
    total_input = 0
    total_output = 0
    total_tokens = 0

    for question in QUESTIONS:

        history.append(
            HumanMessage(content=question)
        )

        # Keep only the most recent 2 messages
        recent_history = history[-2:]

        response = llm.invoke(recent_history)

        input_tokens, output_tokens, tokens = get_tokens(response)

        total_input += input_tokens
        total_output += output_tokens
        total_tokens += tokens

        history.append(
            AIMessage(content=response.content)
        )

    return total_input, total_output, total_tokens


print("\n--- Part D Token Optimization ---")

print("\nRunning full-history experiment...")
full_input, full_output, full_total = run_full_history()

print("\nRunning recent-history experiment...")
recent_input, recent_output, recent_total = run_recent_history()

input_reduction = (
    (full_input - recent_input) / full_input
) * 100

total_reduction = (
    (full_total - recent_total) / full_total
) * 100

print("\n--- RESULTS ---")

print("\nFull History:")
print(f"Input tokens:  {full_input}")
print(f"Output tokens: {full_output}")
print(f"Total tokens:  {full_total}")

print("\nRecent History:")
print(f"Input tokens:  {recent_input}")
print(f"Output tokens: {recent_output}")
print(f"Total tokens:  {recent_total}")

print("\n--- TOKEN REDUCTION ---")

print(
    f"Input token reduction: "
    f"{input_reduction:.2f}%"
)

print(
    f"Total token reduction: "
    f"{total_reduction:.2f}%"
)