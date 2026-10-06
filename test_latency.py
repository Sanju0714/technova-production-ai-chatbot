import time

from app.graph import graph

config = {
    "configurable": {
        "thread_id": "latency-fix-test"
    },
    "metadata": {
        "model_name": "nvidia/nemotron-3.5-lightning-30b-a3b",
        "user_id": "latency-test",
        "app_version": "1.0.0",
        "session_id": "latency-fix-test"
    },
    "tags": [
        "technova-bot",
        "latency-fix-test",
        "nemotron-3.5"
    ]
}

question = "Where is my order TN1001?"

start = time.perf_counter()

result = graph.invoke(
    {"messages": [("user", question)]},
    config=config
)

elapsed = time.perf_counter() - start

print(f"\nLatency: {elapsed:.2f}s")
print("Answer:", result["messages"][-1].content)