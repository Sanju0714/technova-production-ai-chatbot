import os

from dotenv import load_dotenv
from langsmith import Client


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()


# ============================================================
# LangSmith client
# ============================================================

client = Client()


# ============================================================
# Evaluation dataset
# ============================================================

DATASET_NAME = "technova-customer-support-eval"


examples = [
    {
        "question": "What is the status of order TN1001?",
        "reference_answer": (
            "Order TN1001 is shipped. "
            "The item is Laptop Pro 14 and the ETA is 2 days."
        )
    },

    {
        "question": "What item is in order TN1001?",
        "reference_answer": "The item in TN1001 is Laptop Pro 14."
    },

    {
        "question": "What is the status of order TN1002?",
        "reference_answer": (
            "Order TN1002 is processing. "
            "The item is Noise-cancel Earbuds and the ETA is 5 days."
        )
    },

    {
        "question": "What item is in order TN1003?",
        "reference_answer": "The item in TN1003 is Phone X."
    },

    {
        "question": "What is TechNova's return policy?",
        "reference_answer": (
            "Returns are accepted within 30 days "
            "in the original packaging."
        )
    },

    {
        "question": "What is TechNova's warranty policy?",
        "reference_answer": (
            "Electronics come with a "
            "1-year manufacturer warranty."
        )
    },

    {
        "question": "What is TechNova's shipping policy?",
        "reference_answer": (
            "Free shipping is available for orders "
            "above Rs.999. Standard delivery takes 3-5 days."
        )
    },

    {
        "question": "How long does standard delivery take?",
        "reference_answer": (
            "Standard delivery takes 3-5 days."
        )
    },

    {
        "question": "How much do I need to spend for free shipping?",
        "reference_answer": (
            "Free shipping is available for orders "
            "above Rs.999."
        )
    },

    {
        "question": "Where is order TN9999?",
        "reference_answer": (
            "Order TN9999 was not found."
        )
    }
]


# ============================================================
# Create dataset
# ============================================================

try:

    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description=(
            "TechNova customer-support evaluation dataset "
            "for testing order lookup and company policies."
        )
    )

    print(f"Created dataset: {DATASET_NAME}")

except Exception as error:

    print(
        f"Dataset may already exist: {error}"
    )

    datasets = list(
        client.list_datasets(
            dataset_name=DATASET_NAME
        )
    )

    if not datasets:
        raise

    dataset = datasets[0]


# ============================================================
# Add examples
# ============================================================

for example in examples:

    client.create_example(
        inputs={
            "question": example["question"]
        },
        outputs={
            "reference_answer": example["reference_answer"]
        },
        dataset_id=dataset.id
    )


# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("LANGSMITH EVALUATION DATASET")
print("=" * 60)

print(f"Dataset : {DATASET_NAME}")
print(f"Examples: {len(examples)}")

print("=" * 60)

print("\nDataset examples:")

for i, example in enumerate(examples, start=1):

    print(
        f"{i:02d}. {example['question']}"
    )

print("\nDataset creation complete.")