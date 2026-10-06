import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

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

SYSTEM_PROMPT = """
You are the TechNova customer support assistant.
Be helpful, professional, and concise.
"""

QUESTIONS = [
    "What is TechNova's return policy?",
    "How long is the warranty?",
    "How long does standard shipping take?",
    "Is shipping free?",
    "Can I return an electronic product?",
    "Does TechNova provide a manufacturer warranty?",
    "How many days do I have to return an item?",
    "Tell me about TechNova shipping.",
    "Can I get free shipping?",
    "Tell me about TechNova's return policy."
]

messages = [
    SystemMessage(content=SYSTEM_PROMPT)
]

results = []

print("\n--- 120B Token Growth Benchmark ---\n")

for i, question in enumerate(QUESTIONS, start=1):

    messages.append(
        HumanMessage(content=question)
    )

    response = llm.invoke(messages)

    usage = response.usage_metadata or {}

    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    total_tokens = usage.get(
        "total_tokens",
        input_tokens + output_tokens
    )

    results.append({
        "turn": i,
        "input": input_tokens,
        "output": output_tokens,
        "total": total_tokens
    })

    print(
        f"Turn {i}: "
        f"Input={input_tokens}, "
        f"Output={output_tokens}, "
        f"Total={total_tokens}"
    )

    messages.append(
        AIMessage(content=response.content)
    )


total_input = sum(r["input"] for r in results)
total_output = sum(r["output"] for r in results)
total_tokens = sum(r["total"] for r in results)

print("\n--- Totals ---")
print(f"Input Tokens:  {total_input}")
print(f"Output Tokens: {total_output}")
print(f"Total Tokens:  {total_tokens}")

first_input = results[0]["input"]
last_input = results[-1]["input"]

growth = (
    ((last_input - first_input) / first_input) * 100
    if first_input > 0
    else 0
)

print("\n--- Token Growth ---")
print(f"Turn 1 Input Tokens:  {first_input}")
print(f"Turn 10 Input Tokens: {last_input}")
print(f"Input Token Growth:   {growth:.2f}%")