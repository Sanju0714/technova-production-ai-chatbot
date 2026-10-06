import os

from dotenv import load_dotenv
from langsmith import Client

from experiments.evaluation_dataset import EVALUATION_DATASET

load_dotenv()

client = Client()

dataset_name = "TechNova Customer Support Evaluation"

# Create dataset
dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="10-question evaluation dataset for the TechNova customer support chatbot."
)

# Add examples
inputs = [
    {"question": item["question"]}
    for item in EVALUATION_DATASET
]

outputs = [
    {"answer": item["reference"]}
    for item in EVALUATION_DATASET
]

client.create_examples(
    inputs=inputs,
    outputs=outputs,
    dataset_id=dataset.id
)

print("Dataset created successfully!")
print(f"Dataset name: {dataset_name}")
print(f"Dataset ID: {dataset.id}")
print(f"Examples added: {len(EVALUATION_DATASET)}")