from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

dataset_name = "TechNova Customer Support Evaluation"

datasets = list(
    client.list_datasets(dataset_name=dataset_name)
)

if not datasets:
    print("Dataset not found.")
else:
    dataset = datasets[0]

    print("Dataset found!")
    print(f"Dataset name: {dataset.name}")
    print(f"Dataset ID: {dataset.id}")

    examples = list(
        client.list_examples(dataset_id=dataset.id)
    )

    print(f"Examples found: {len(examples)}")

    print("\nEvaluation examples:")

    for i, example in enumerate(examples, start=1):
        question = example.inputs.get("question", "")
        reference = example.outputs.get("answer", "")

        print(f"\n{i}. {question}")
        print(f"   Reference: {reference}")