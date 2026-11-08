
import os

import streamlit as st
from dotenv import load_dotenv
from langsmith import traceable

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from app.tools import get_order_status, get_policy


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

load_dotenv()


def get_nvidia_api_key():
    """Get NVIDIA API key from Streamlit Secrets or local .env."""

    try:
        api_key = st.secrets.get("NVIDIA_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv("NVIDIA_API_KEY")

    if not api_key:
        raise ValueError(
            "NVIDIA_API_KEY is missing. "
            "Add it to Streamlit Cloud Secrets or your local .env file."
        )

    return api_key


# ============================================================
# NVIDIA MODEL CONFIGURATION
# ============================================================

MODEL_NAME = "nvidia/nemotron-3.5-lightning-30b-a3b"

llm = ChatOpenAI(
    model=MODEL_NAME,
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=get_nvidia_api_key(),
    temperature=0,
    max_tokens=200,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    }
)


# ============================================================
# AVAILABLE TOOLS
# ============================================================

tools = [
    get_order_status,
    get_policy
]

llm_with_tools = llm.bind_tools(tools)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are the TechNova customer support assistant.

TechNova is an electronics store that sells laptops, phones,
and accessories.

You can help customers with:
- Order status
- Returns
- Warranty
- Shipping
- Refunds
- Cancellation
- Payment
- Exchange
- Damaged products
- Late delivery
- Replacement

Use the available tools whenever you need order or policy information.

Never invent order information or company policies.

If an order or policy cannot be found, clearly explain that
you could not retrieve the requested information.

Be helpful, professional, and concise.
"""


# ============================================================
# CLEAN USER INPUT
# ============================================================

@traceable(name="clean_user_input")
def clean_user_input(message: str) -> str:
    """Clean and normalize user input."""
    return message.strip()


# ============================================================
# AGENT NODE
# ============================================================

def agent(state: MessagesState):

    cleaned_messages = []

    for message in state["messages"]:

        if isinstance(message.content, str):
            message.content = clean_user_input(message.content)

        cleaned_messages.append(message)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ] + cleaned_messages

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# ============================================================
# LANGGRAPH WORKFLOW
# ============================================================

builder = StateGraph(MessagesState)

# Add agent node
builder.add_node("agent", agent)

# Add tool execution node
builder.add_node(
    "tools",
    ToolNode(
        tools,
        handle_tool_errors=True
    )
)

# Define workflow
builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    tools_condition
)

builder.add_edge("tools", "agent")


# ============================================================
# MEMORY AND GRAPH COMPILATION
# ============================================================

memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory
)


# ============================================================
# TERMINAL TESTING
# ============================================================

if __name__ == "__main__":

    config = {
        "configurable": {
            "thread_id": "test-session-1"
        },
        "metadata": {
            "model_name": MODEL_NAME,
            "user_id": "test-user-001",
            "app_version": "1.0.0",
            "session_id": "test-session-1"
        },
        "tags": [
            "technova-bot",
            "nemotron-3.5",
            "production-test"
        ]
    }

    print("\nTechNova Support Chatbot")
    print("Type 'exit' to stop.\n")

    while True:

        user_question = input("You: ")

        if user_question.lower().strip() == "exit":
            print("Goodbye!")
            break

        try:

            result = graph.invoke(
                {
                    "messages": [
                        ("user", user_question)
                    ]
                },
                config=config
            )

            print(
                "Assistant:",
                result["messages"][-1].content
            )

        except Exception as error:

            print(
                "Assistant: I'm sorry, but I'm currently "
                "unable to process your request. "
                "Please try again later."
            )

            print(
                "[ERROR]",
                type(error).__name__,
                str(error)
            )
