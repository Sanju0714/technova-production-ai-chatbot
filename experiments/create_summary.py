import os
import pandas as pd


# ============================================================
# Final TechNova Assignment Results
# ============================================================

results = [

    # Part C - Latency
    {
        "part": "C",
        "metric": "Baseline Average Latency",
        "value": 9.34,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "Baseline P50 Latency",
        "value": 4.70,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "Baseline P95 Latency",
        "value": 42.47,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "Baseline Max Latency",
        "value": 55.91,
        "unit": "seconds"
    },

    {
        "part": "C",
        "metric": "Optimized Average Latency",
        "value": 5.33,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "Optimized P50 Latency",
        "value": 2.65,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "Optimized P95 Latency",
        "value": 18.48,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "Optimized Max Latency",
        "value": 28.27,
        "unit": "seconds"
    },

    {
        "part": "C",
        "metric": "Average Latency Improvement",
        "value": 42.9,
        "unit": "%"
    },
    {
        "part": "C",
        "metric": "P50 Latency Improvement",
        "value": 43.6,
        "unit": "%"
    },
    {
        "part": "C",
        "metric": "P95 Latency Improvement",
        "value": 56.5,
        "unit": "%"
    },
    {
        "part": "C",
        "metric": "Max Latency Improvement",
        "value": 49.4,
        "unit": "%"
    },

    # Model comparison
    {
        "part": "C",
        "metric": "30B Average Latency",
        "value": 6.71,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "30B P50 Latency",
        "value": 3.20,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "30B P95 Latency",
        "value": 16.94,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "30B Max Latency",
        "value": 18.53,
        "unit": "seconds"
    },

    {
        "part": "C",
        "metric": "120B Average Latency",
        "value": 1.30,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "120B P50 Latency",
        "value": 1.14,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "120B P95 Latency",
        "value": 2.29,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "120B Max Latency",
        "value": 2.82,
        "unit": "seconds"
    },

    {
        "part": "C",
        "metric": "30B TTFT",
        "value": 0.554,
        "unit": "seconds"
    },
    {
        "part": "C",
        "metric": "120B TTFT",
        "value": 0.356,
        "unit": "seconds"
    },

    # Part D - Token usage
    {
        "part": "D",
        "metric": "10-Turn Input Tokens",
        "value": 8178,
        "unit": "tokens"
    },
    {
        "part": "D",
        "metric": "10-Turn Output Tokens",
        "value": 1722,
        "unit": "tokens"
    },
    {
        "part": "D",
        "metric": "10-Turn Total Tokens",
        "value": 9900,
        "unit": "tokens"
    },
    {
        "part": "D",
        "metric": "Input Token Reduction",
        "value": 77.1,
        "unit": "%"
    },
    {
        "part": "D",
        "metric": "Total Token Reduction",
        "value": 62.6,
        "unit": "%"
    },

    # Part D - Cost
    {
        "part": "D",
        "metric": "30B 10-Turn Cost",
        "value": 0.001980,
        "unit": "USD"
    },
    {
        "part": "D",
        "metric": "120B 10-Turn Cost",
        "value": 0.008910,
        "unit": "USD"
    },
    {
        "part": "D",
        "metric": "30B 20Q Benchmark Cost",
        "value": 0.004103,
        "unit": "USD"
    },
    {
        "part": "D",
        "metric": "120B 20Q Benchmark Cost",
        "value": 0.018238,
        "unit": "USD"
    },
    {
        "part": "D",
        "metric": "30B Daily Cost at 10K Conversations",
        "value": 19.80,
        "unit": "USD/day"
    },
    {
        "part": "D",
        "metric": "30B Monthly Cost at 10K Conversations",
        "value": 594,
        "unit": "USD/month"
    },
    {
        "part": "D",
        "metric": "120B Daily Cost at 10K Conversations",
        "value": 89.10,
        "unit": "USD/day"
    },
    {
        "part": "D",
        "metric": "120B Monthly Cost at 10K Conversations",
        "value": 2673,
        "unit": "USD/month"
    },

    # Part E - Reliability
    {
        "part": "E",
        "metric": "Error Benchmark Requests",
        "value": 20,
        "unit": "requests"
    },
    {
        "part": "E",
        "metric": "Successful Requests",
        "value": 20,
        "unit": "requests"
    },
    {
        "part": "E",
        "metric": "Failed Requests",
        "value": 0,
        "unit": "requests"
    },
    {
        "part": "E",
        "metric": "Error Rate",
        "value": 0,
        "unit": "%"
    },

    # Part F - Evaluation
    {
        "part": "F",
        "metric": "Evaluation Dataset Size",
        "value": 10,
        "unit": "examples"
    },
    {
        "part": "F",
        "metric": "30B Evaluation Accuracy",
        "value": 100,
        "unit": "%"
    },
    {
        "part": "F",
        "metric": "120B Evaluation Accuracy",
        "value": 100,
        "unit": "%"
    },
    {
        "part": "F",
        "metric": "Positive Human Feedback Runs",
        "value": 10,
        "unit": "runs"
    }
]


# ============================================================
# Create DataFrame
# ============================================================

df = pd.DataFrame(results)


# ============================================================
# Save Results
# ============================================================

output_path = "results/summary.csv"

df.to_csv(
    output_path,
    index=False
)


# ============================================================
# Display
# ============================================================

print("\n" + "=" * 70)
print("TECHNOVA FINAL RESULTS SUMMARY")
print("=" * 70)

print(df.to_string(index=False))

print("\n" + "=" * 70)
print(f"Saved to: {output_path}")
print("=" * 70)