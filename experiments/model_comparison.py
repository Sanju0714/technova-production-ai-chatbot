import os
import time
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from app.tools import get_order_status, get_policy


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODELS = {
    "Nemotron 3.5 Lightning 30B": "nvidia/nemotron-3.5-lightning-30b-a3b",
    "Nemotron 3 Super 120B": "nvidia/nemotron-3-super-120b-a12b",
}

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
]


SYSTEM_PROMPT = """
You are the TechNova customer support assistant.

TechNova is an electronics store that sells laptops, phones,
and accessories.

You can help customers with:
- Order status
- Returns
- Warranty
- Shipping

Use the available tools whenever you need order or policy information.

Never invent order information or company policies.

If an order or policy cannot be found, clearly explain that
you could not retrieve the requested information.

Be helpful, professional, and concise.
"""


# --------------------------------------------------
# Create graph for a specific model
# --------------------------------------------------

def create_graph(model_name):

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

    tools = [get_order_status, get_policy]

    llm_with_tools = llm.bind_tools(tools)

    def agent(state: MessagesState):

        messages = [
            SystemMessage(content=SYSTEM_PROMPT)
        ] + state["messages"]

        response = llm_with_tools.invoke(messages)

        return {
            "messages": [response]
        }

    builder = StateGraph(MessagesState)

    builder.add_node("agent", agent)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    memory = MemorySaver()

    return builder.compile(checkpointer=memory)


# --------------------------------------------------
# Run benchmark
# --------------------------------------------------

def benchmark_model(model_label, model_name):

    print("\n" + "=" * 60)
    print(f"Testing: {model_label}")
    print("=" * 60)

    graph = create_graph(model_name)

    results = []

    for i, question in enumerate(QUESTIONS, start=1):

        thread_id = f"comparison-{model_label[:10]}-{i}"

        config = {
            "configurable": {
                "thread_id": thread_id
            },
            "metadata": {
                "model_name": model_name,
                "user_id": "model-comparison",
                "app_version": "1.0.0",
                "session_id": thread_id
            },
            "tags": [
                "technova-bot",
                "model-comparison"
            ]
        }

        start = time.perf_counter()

        result = graph.invoke(
            {"messages": [("user", question)]},
            config=config
        )

        latency = time.perf_counter() - start

        answer = result["messages"][-1].content

        results.append({
            "model": model_label,
            "question": question,
            "latency_seconds": latency,
            "answer": answer
        })

        print(
            f"{i:02d}. {latency:.2f}s - {question}"
        )

    return results


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    all_results = []

    for model_label, model_name in MODELS.items():

        results = benchmark_model(
            model_label,
            model_name
        )

        all_results.extend(results)

    df = pd.DataFrame(all_results)

    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

    summary = (
        df.groupby("model")["latency_seconds"]
        .agg(
            Average="mean",
            P50=lambda x: x.quantile(0.50),
            P95=lambda x: x.quantile(0.95),
            Maximum="max"
        )
        .round(2)
    )

    print(summary)

    df.to_csv(
        "results/model_comparison.csv",
        index=False
    )

    summary.to_csv(
        "results/model_comparison_summary.csv"
    )

    print("\nResults saved:")
    print("results/model_comparison.csv")
    print("results/model_comparison_summary.csv")