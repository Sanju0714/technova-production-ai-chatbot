import os
import time
import pandas as pd

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from app.tools import get_order_status, get_policy


load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")


# ============================================================
# MODELS
# ============================================================

MODELS = {
    "Nemotron 3.5 Lightning 30B": "nvidia/nemotron-3.5-lightning-30b-a3b",
    "Nemotron 3 Super 120B": "nvidia/nemotron-3-super-120b-a12b",
}


# ============================================================
# 20 BENCHMARK QUESTIONS
# ============================================================

QUESTIONS = [
    "Where is order TN1001?",
    "What is the status of TN1002?",
    "What happened to order TN1003?",
    "What is the return policy?",
    "What is the warranty policy?",
    "What is the shipping policy?",
    "How long do I have to return an item?",
    "Do electronics have a warranty?",
    "When do I get free shipping?",
    "What is the delivery time for shipping?",
    "What item is in TN1001?",
    "What item is in TN1002?",
    "What is the status of TN1003?",
    "When will TN1001 arrive?",
    "When will TN1002 arrive?",
    "Can I return an electronic item?",
    "How many days do I have to return something?",
    "How long is the manufacturer warranty?",
    "Tell me about TechNova shipping.",
    "Can I return my order within 30 days?",
]


# ============================================================
# RESUME SETTINGS
# ============================================================

# We only need to run Question 20 for the 120B model
# because Questions 1-19 were already completed.

RUN_ONLY_MODEL = "Nemotron 3 Super 120B"

START_QUESTION = 20
END_QUESTION = 20


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

Use the available tools whenever you need order or policy information.

Never invent order information or company policies.

If an order or policy cannot be found, clearly explain that
you could not retrieve the requested information.

Be helpful, professional, and concise.
"""


# ============================================================
# BUILD LANGGRAPH
# ============================================================

def build_graph(model_name):

    llm = ChatOpenAI(
        model=model_name,
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_API_KEY,
        temperature=0,
        max_tokens=256,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        }
    )

    tools = [
        get_order_status,
        get_policy
    ]

    llm_with_tools = llm.bind_tools(tools)

    def agent(state: MessagesState):

        from langchain_core.messages import SystemMessage

        messages = [
            SystemMessage(content=SYSTEM_PROMPT)
        ] + state["messages"]

        response = llm_with_tools.invoke(messages)

        return {
            "messages": [response]
        }

    builder = StateGraph(MessagesState)

    builder.add_node(
        "agent",
        agent
    )

    builder.add_node(
        "tools",
        ToolNode(tools)
    )

    builder.add_edge(
        START,
        "agent"
    )

    builder.add_conditional_edges(
        "agent",
        tools_condition
    )

    builder.add_edge(
        "tools",
        "agent"
    )

    memory = MemorySaver()

    return builder.compile(
        checkpointer=memory
    )


# ============================================================
# GET TOKEN USAGE
# ============================================================

def get_usage(message):

    usage = getattr(
        message,
        "usage_metadata",
        None
    )

    if usage:

        return {
            "input_tokens": usage.get(
                "input_tokens",
                0
            ),

            "output_tokens": usage.get(
                "output_tokens",
                0
            ),

            "total_tokens": usage.get(
                "total_tokens",
                0
            )
        }

    response_metadata = getattr(
        message,
        "response_metadata",
        {}
    ) or {}

    token_usage = response_metadata.get(
        "token_usage",
        {}
    )

    return {
        "input_tokens": token_usage.get(
            "prompt_tokens",
            0
        ),

        "output_tokens": token_usage.get(
            "completion_tokens",
            0
        ),

        "total_tokens": token_usage.get(
            "total_tokens",
            0
        )
    }


# ============================================================
# RUN BENCHMARK
# ============================================================

all_results = []


for model_label, model_name in MODELS.items():

    # --------------------------------------------------------
    # Only run the selected model
    # --------------------------------------------------------

    if model_label != RUN_ONLY_MODEL:
        continue

    print("\n" + "=" * 70)
    print(model_label)
    print("=" * 70)

    graph = build_graph(
        model_name
    )

    model_input = 0
    model_output = 0
    model_total = 0


    # --------------------------------------------------------
    # Select only Question 20
    # --------------------------------------------------------

    selected_questions = QUESTIONS[
        START_QUESTION - 1 : END_QUESTION
    ]


    for i, question in enumerate(
        selected_questions,
        start=START_QUESTION
    ):

        thread_id = (
            f"cost-{model_label[:4]}-{i}"
        )

        config = {

            "configurable": {
                "thread_id": thread_id
            },

            "metadata": {
                "model_name": model_name,
                "experiment": "20-question-cost-benchmark-resume"
            },

            "tags": [
                "technova-bot",
                "cost-benchmark",
                "resume"
            ]
        }


        # ----------------------------------------------------
        # Measure latency
        # ----------------------------------------------------

        start = time.perf_counter()


        result = graph.invoke(
            {
                "messages": [
                    ("user", question)
                ]
            },
            config=config
        )


        latency = (
            time.perf_counter()
            - start
        )


        # ----------------------------------------------------
        # Extract token usage
        # ----------------------------------------------------

        input_tokens = 0
        output_tokens = 0
        total_tokens = 0


        for message in result["messages"]:

            if message.__class__.__name__ == "AIMessage":

                usage = get_usage(
                    message
                )

                input_tokens += usage[
                    "input_tokens"
                ]

                output_tokens += usage[
                    "output_tokens"
                ]

                total_tokens += usage[
                    "total_tokens"
                ]


        # ----------------------------------------------------
        # Model totals
        # ----------------------------------------------------

        model_input += input_tokens
        model_output += output_tokens
        model_total += total_tokens


        # ----------------------------------------------------
        # Print result
        # ----------------------------------------------------

        print(
            f"{i:02d}. "
            f"{latency:.2f}s | "
            f"Input: {input_tokens} | "
            f"Output: {output_tokens} | "
            f"Total: {total_tokens}"
        )


        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        all_results.append({

            "model": model_label,

            "model_id": model_name,

            "question_number": i,

            "question": question,

            "input_tokens": input_tokens,

            "output_tokens": output_tokens,

            "total_tokens": total_tokens,

            "latency_seconds": round(
                latency,
                3
            )
        })


    # ========================================================
    # MODEL TOTALS
    # ========================================================

    print("\nModel totals:")

    print(
        f"Input tokens : {model_input:,}"
    )

    print(
        f"Output tokens: {model_output:,}"
    )

    print(
        f"Total tokens : {model_total:,}"
    )


# ============================================================
# SAVE QUESTION 20 RESULT
# ============================================================

df = pd.DataFrame(
    all_results
)


os.makedirs(
    "results",
    exist_ok=True
)


df.to_csv(
    "results/benchmark_cost_q20_resume.csv",
    index=False
)


# ============================================================
# CALCULATE QUESTION 20 COST
# ============================================================

summary = []


for model_label, group in df.groupby(
    "model"
):

    input_tokens = group[
        "input_tokens"
    ].sum()

    output_tokens = group[
        "output_tokens"
    ].sum()

    total_tokens = group[
        "total_tokens"
    ].sum()


    # --------------------------------------------------------
    # NVIDIA hypothetical rates from assignment
    # --------------------------------------------------------

    if "30B" in model_label:

        input_rate = 0.20
        output_rate = 0.20

    else:

        input_rate = 0.90
        output_rate = 0.90


    # --------------------------------------------------------
    # Cost
    # --------------------------------------------------------

    input_cost = (
        input_tokens
        / 1_000_000
    ) * input_rate


    output_cost = (
        output_tokens
        / 1_000_000
    ) * output_rate


    benchmark_cost = (
        input_cost
        + output_cost
    )


    summary.append({

        "model": model_label,

        "input_tokens": input_tokens,

        "output_tokens": output_tokens,

        "total_tokens": total_tokens,

        "input_cost_usd": input_cost,

        "output_cost_usd": output_cost,

        "question_20_cost_usd": benchmark_cost

    })


summary_df = pd.DataFrame(
    summary
)


summary_df.to_csv(
    "results/benchmark_cost_q20_resume_summary.csv",
    index=False
)


# ============================================================
# PRINT FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("QUESTION 20 COST RESULT")
print("=" * 70)


print(
    summary_df.to_string(
        index=False
    )
)


print("\nResults saved to:")

print(
    "results/benchmark_cost_q20_resume.csv"
)

print(
    "results/benchmark_cost_q20_resume_summary.csv"
)