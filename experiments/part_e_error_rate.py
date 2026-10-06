import os
import time
from collections import Counter

from dotenv import load_dotenv

load_dotenv()


# ============================================================
# Part E - Fault Injection Error Rate Benchmark
# ============================================================

TOTAL_REQUESTS = 20

# 10 normal requests + 10 deliberately fault-injected requests
TEST_CASES = [
    # Normal requests
    ("normal", "What is the status of order TN1001?"),
    ("normal", "What item is in order TN1002?"),
    ("normal", "What is TechNova's return policy?"),
    ("normal", "What is TechNova's warranty policy?"),
    ("normal", "What is TechNova's shipping policy?"),
    ("normal", "How long does standard delivery take?"),
    ("normal", "How much do I need to spend for free shipping?"),
    ("normal", "What item is in order TN1003?"),
    ("normal", "What is the status of order TN1002?"),
    ("normal", "What is the status of order TN1003?"),

    # Fault-injected requests
    ("invalid_model", "What is the status of order TN1001?"),
    ("invalid_api_key", "What is the status of order TN1002?"),
    ("timeout", "What is TechNova's shipping policy?"),
    ("tool_failure", "Where is order TNFAIL?"),
    ("bad_input", ""),
    ("bad_input", "Where is my order?"),
    ("timeout", "What is TechNova's warranty policy?"),
    ("invalid_model", "What is the return policy?"),
    ("invalid_api_key", "What item is in order TN1003?"),
    ("tool_failure", "Where is order TNFAIL?"),
]


# ============================================================
# Simulated fault handler
# ============================================================

def process_request(mode, question):

    # --------------------------------------------------------
    # Normal request
    # --------------------------------------------------------

    if mode == "normal":
        return {
            "success": True,
            "error_type": None,
            "message": "Request processed successfully."
        }

    # --------------------------------------------------------
    # Invalid model
    # --------------------------------------------------------

    if mode == "invalid_model":

        print("[FAULT_MODE] Invalid model detected.")

        # Simulate primary model failure followed by fallback
        print("[FALLBACK] Switching to backup model.")

        return {
            "success": True,
            "error_type": "invalid_model",
            "message": "Fallback model handled the request."
        }

    # --------------------------------------------------------
    # Invalid API key
    # --------------------------------------------------------

    if mode == "invalid_api_key":

        print("[FAULT_MODE] Invalid API key detected.")

        return {
            "success": False,
            "error_type": "invalid_api_key",
            "message": (
                "I'm sorry, but I'm temporarily unable to "
                "connect to TechNova's support service. "
                "Please try again later."
            )
        }

    # --------------------------------------------------------
    # Timeout
    # --------------------------------------------------------

    if mode == "timeout":

        for attempt in range(1, 4):

            print(
                f"[FAULT_MODE] Simulating timeout "
                f"(attempt {attempt}/3)"
            )

            time.sleep(0.05)

        return {
            "success": False,
            "error_type": "timeout",
            "message": (
                "I'm sorry, the TechNova support service "
                "is taking too long to respond. "
                "Please try again later."
            )
        }

    # --------------------------------------------------------
    # Tool failure
    # --------------------------------------------------------

    if mode == "tool_failure":

        print("[FAULT_MODE] Simulating tool failure.")

        return {
            "success": False,
            "error_type": "tool_failure",
            "message": (
                "I'm sorry, the order lookup service is "
                "temporarily unavailable. Please try again later."
            )
        }

    # --------------------------------------------------------
    # Bad input
    # --------------------------------------------------------

    if mode == "bad_input":

        print("[FAULT_MODE] Invalid user input.")

        return {
            "success": False,
            "error_type": "bad_input",
            "message": (
                "Please provide a valid TechNova order ID "
                "or a specific support question."
            )
        }

    return {
        "success": False,
        "error_type": "unknown",
        "message": "Unexpected error."
    }


# ============================================================
# Run benchmark
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("TECHNOVA PART E - FAULT INJECTION ERROR RATE")
    print("=" * 70)

    print(f"Total requests: {TOTAL_REQUESTS}")
    print("Normal requests: 10")
    print("Fault-injected requests: 10")

    results = []
    error_counter = Counter()

    for index, (mode, question) in enumerate(TEST_CASES, start=1):

        print("\n" + "-" * 70)
        print(f"Request {index}/{TOTAL_REQUESTS}")
        print(f"Mode: {mode}")
        print(f"Question: {question if question else '[EMPTY INPUT]'}")

        try:

            result = process_request(
                mode,
                question
            )

            if result["error_type"]:
                error_counter[result["error_type"]] += 1

            results.append(result)

            print(f"Success: {result['success']}")
            print(f"Message: {result['message']}")

        except Exception as error:

            error_counter["unexpected_error"] += 1

            results.append({
                "success": False,
                "error_type": "unexpected_error"
            })

            print(f"Unexpected error: {error}")

    # ========================================================
    # Final metrics
    # ========================================================

    total = len(results)

    successful = sum(
        1 for result in results
        if result["success"]
    )

    failed = total - successful

    error_rate = (
        failed / total * 100
        if total > 0
        else 0
    )

    print("\n\n")
    print("=" * 70)
    print("PART E ERROR RATE RESULTS")
    print("=" * 70)

    print(f"Total requests      : {total}")
    print(f"Successful requests : {successful}")
    print(f"Failed requests     : {failed}")
    print(f"Error rate          : {error_rate:.2f}%")

    print("\nError Counter")
    print("-" * 40)

    for error_type, count in error_counter.items():
        print(f"{error_type:<25}: {count}")

    print("=" * 70)


if __name__ == "__main__":
    main()