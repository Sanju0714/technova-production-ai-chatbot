import pandas as pd


# ============================================================
# TECHNOVA BOT — FINAL METRICS
# ============================================================

print("=" * 70)
print("TECHNOVA BOT — FINAL METRICS SUMMARY")
print("=" * 70)


# ------------------------------------------------------------
# 1. LATENCY — BASELINE VS OPTIMIZED
# ------------------------------------------------------------

baseline = {
    "average": 9.34,
    "p50": 4.70,
    "p95": 42.47,
    "max": 55.91
}

optimized = {
    "average": 5.33,
    "p50": 2.65,
    "p95": 18.48,
    "max": 28.27
}

print("\n1. LATENCY OPTIMIZATION")
print("-" * 50)

print(f"Average: {baseline['average']:.2f}s -> {optimized['average']:.2f}s")
print(f"P50:     {baseline['p50']:.2f}s -> {optimized['p50']:.2f}s")
print(f"P95:     {baseline['p95']:.2f}s -> {optimized['p95']:.2f}s")
print(f"Max:     {baseline['max']:.2f}s -> {optimized['max']:.2f}s")

avg_improvement = (
    (baseline["average"] - optimized["average"])
    / baseline["average"]
) * 100

p50_improvement = (
    (baseline["p50"] - optimized["p50"])
    / baseline["p50"]
) * 100

p95_improvement = (
    (baseline["p95"] - optimized["p95"])
    / baseline["p95"]
) * 100

max_improvement = (
    (baseline["max"] - optimized["max"])
    / baseline["max"]
) * 100

print(f"\nAverage improvement: {avg_improvement:.1f}%")
print(f"P50 improvement:     {p50_improvement:.1f}%")
print(f"P95 improvement:     {p95_improvement:.1f}%")
print(f"Maximum improvement: {max_improvement:.1f}%")


# ------------------------------------------------------------
# 2. MODEL COMPARISON
# ------------------------------------------------------------

model_comparison = {
    "Nemotron 3.5 Lightning 30B": {
        "average": 6.71,
        "p50": 3.20,
        "p95": 16.94,
        "max": 18.53,
        "accuracy": 100.0
    },
    "Nemotron 3 Super 120B": {
        "average": 1.30,
        "p50": 1.14,
        "p95": 2.29,
        "max": 2.82,
        "accuracy": 10.0
    }
}

print("\n2. MODEL COMPARISON")
print("-" * 50)

for model, metrics in model_comparison.items():
    print(f"\n{model}")
    print(f"Average latency: {metrics['average']:.2f}s")
    print(f"P50:             {metrics['p50']:.2f}s")
    print(f"P95:             {metrics['p95']:.2f}s")
    print(f"Maximum:         {metrics['max']:.2f}s")
    print(f"Accuracy:        {metrics['accuracy']:.1f}%")


# ------------------------------------------------------------
# 3. TTFT
# ------------------------------------------------------------

ttft = {
    "Nemotron 3.5 Lightning 30B": {
        "ttft": 0.554,
        "total": 1.252
    },
    "Nemotron 3 Super 120B": {
        "ttft": 0.356,
        "total": 1.718
    }
}

print("\n3. STREAMING / TTFT")
print("-" * 50)

for model, metrics in ttft.items():
    print(
        f"{model}: "
        f"TTFT={metrics['ttft']:.3f}s, "
        f"Total={metrics['total']:.3f}s"
    )


# ------------------------------------------------------------
# 4. TOKEN USAGE — FULL HISTORY
# ------------------------------------------------------------

full_history = {
    "input_tokens": 8178,
    "output_tokens": 1722,
    "total_tokens": 9900
}

print("\n4. TOKEN USAGE — 10-TURN CONVERSATION")
print("-" * 50)

print(f"Input tokens:  {full_history['input_tokens']}")
print(f"Output tokens: {full_history['output_tokens']}")
print(f"Total tokens:  {full_history['total_tokens']}")


# ------------------------------------------------------------
# 5. TOKEN OPTIMIZATION
# ------------------------------------------------------------

optimized_history = {
    "input_tokens": 1871,
    "output_tokens": 1830,
    "total_tokens": 3701
}

input_reduction = (
    (full_history["input_tokens"] - optimized_history["input_tokens"])
    / full_history["input_tokens"]
) * 100

total_reduction = (
    (full_history["total_tokens"] - optimized_history["total_tokens"])
    / full_history["total_tokens"]
) * 100

print("\n5. TOKEN OPTIMIZATION")
print("-" * 50)

print(f"Full-history input:       {full_history['input_tokens']}")
print(f"Recent-history input:     {optimized_history['input_tokens']}")
print(f"Input reduction:          {input_reduction:.1f}%")

print(f"\nFull-history total:        {full_history['total_tokens']}")
print(f"Recent-history total:      {optimized_history['total_tokens']}")
print(f"Total token reduction:     {total_reduction:.1f}%")


# ------------------------------------------------------------
# 6. COST
# ------------------------------------------------------------

small_cost = 0.001980
large_cost = 0.008910

print("\n6. COST ESTIMATION")
print("-" * 50)

print(f"30B cost / 10-turn conversation: ${small_cost:.6f}")
print(f"120B cost / 10-turn conversation: ${large_cost:.6f}")

print("\nAt 10,000 conversations/day:")

print(f"30B daily:   ${19.80:.2f}")
print(f"30B monthly: ${594.00:.2f}")

print(f"120B daily:   ${89.10:.2f}")
print(f"120B monthly: ${2673.00:.2f}")


# ------------------------------------------------------------
# 7. FAULT / ERROR METRICS
# ------------------------------------------------------------

fault_metrics = {
    "total_requests": 10,
    "successful_requests": 6,
    "failed_requests": 4,
    "error_rate": 40.0
}

print("\n7. FAULT / ERROR METRICS")
print("-" * 50)

print(f"Total requests:      {fault_metrics['total_requests']}")
print(f"Successful requests: {fault_metrics['successful_requests']}")
print(f"Failed requests:     {fault_metrics['failed_requests']}")
print(f"Error rate:          {fault_metrics['error_rate']:.2f}%")


# ------------------------------------------------------------
# 8. EVALUATION
# ------------------------------------------------------------

evaluation = {
    "30B_correct": 10,
    "30B_total": 10,
    "30B_accuracy": 100.0,
    "120B_correct": 1,
    "120B_total": 10,
    "120B_accuracy": 10.0
}

print("\n8. LLM EVALUATION")
print("-" * 50)

print(
    f"30B:  {evaluation['30B_correct']}/"
    f"{evaluation['30B_total']} "
    f"= {evaluation['30B_accuracy']:.1f}%"
)

print(
    f"120B: {evaluation['120B_correct']}/"
    f"{evaluation['120B_total']} "
    f"= {evaluation['120B_accuracy']:.1f}%"
)


# ------------------------------------------------------------
# 9. DEPLOYMENT RECOMMENDATION
# ------------------------------------------------------------

print("\n9. DEPLOYMENT RECOMMENDATION")
print("-" * 50)

print(
    "Recommended model: Nemotron 3.5 Lightning 30B"
)

print(
    "Reason: It achieved 100% evaluation accuracy on the "
    "TechNova benchmark and demonstrated strong task/context adherence."
)

print(
    "The 120B model was faster in the measured latency benchmark "
    "but achieved only 10% evaluation accuracy."
)

print("\n" + "=" * 70)
print("FINAL METRICS SUMMARY COMPLETE")
print("=" * 70)