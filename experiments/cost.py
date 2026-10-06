import pandas as pd

# Assignment pricing
SMALL_MODEL_RATE = 0.20   # $ per 1M input/output tokens
LARGE_MODEL_RATE = 0.90   # $ per 1M input/output tokens

# Your measured 10-turn conversation usage
INPUT_TOKENS = 8178
OUTPUT_TOKENS = 1722


def calculate_cost(input_tokens, output_tokens, rate):
    input_cost = (input_tokens / 1_000_000) * rate
    output_cost = (output_tokens / 1_000_000) * rate
    return input_cost + output_cost


def main():

    small_cost = calculate_cost(
        INPUT_TOKENS,
        OUTPUT_TOKENS,
        SMALL_MODEL_RATE
    )

    large_cost = calculate_cost(
        INPUT_TOKENS,
        OUTPUT_TOKENS,
        LARGE_MODEL_RATE
    )

    print("=" * 60)
    print("10-TURN CONVERSATION COST")
    print("=" * 60)

    print(f"Input tokens:  {INPUT_TOKENS:,}")
    print(f"Output tokens: {OUTPUT_TOKENS:,}")
    print(f"Total tokens:  {INPUT_TOKENS + OUTPUT_TOKENS:,}")

    print(f"\nSmall model cost: ${small_cost:.6f}")
    print(f"Large model cost: ${large_cost:.6f}")

    # Production workload
    conversations_per_day = 10_000

    daily_small = small_cost * conversations_per_day
    daily_large = large_cost * conversations_per_day

    monthly_small = daily_small * 30
    monthly_large = daily_large * 30

    print("\n" + "=" * 60)
    print("10,000 CONVERSATIONS / DAY")
    print("=" * 60)

    print(f"\nSmall model:")
    print(f"Daily:   ${daily_small:.2f}")
    print(f"Monthly: ${monthly_small:.2f}")

    print(f"\nLarge model:")
    print(f"Daily:   ${daily_large:.2f}")
    print(f"Monthly: ${monthly_large:.2f}")


if __name__ == "__main__":
    main()