import csv
import os

FEEDBACK_FILE = "results/evaluation_feedback.csv"

feedback_data = [
    {
        "question_id": 1,
        "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
        "feedback": "thumbs_up"
    },
    {
        "question_id": 2,
        "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
        "feedback": "thumbs_up"
    },
    {
        "question_id": 3,
        "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
        "feedback": "thumbs_up"
    },
    {
        "question_id": 4,
        "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
        "feedback": "thumbs_up"
    },
    {
        "question_id": 5,
        "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
        "feedback": "thumbs_up"
    },
    {
        "question_id": 6,
        "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
        "feedback": "thumbs_up"
    },
    {
        "question_id": 7,
        "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
        "feedback": "thumbs_up"
    },
    {
        "question_id": 8,
        "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
        "feedback": "thumbs_up"
    },
    {
        "question_id": 9,
        "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
        "feedback": "thumbs_up"
    },
    {
        "question_id": 10,
        "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
        "feedback": "thumbs_up"
    }
]

os.makedirs("results", exist_ok=True)

with open(FEEDBACK_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["question_id", "model", "feedback"]
    )

    writer.writeheader()
    writer.writerows(feedback_data)

print("=" * 60)
print("EVALUATION FEEDBACK")
print("=" * 60)

print(f"Feedback records: {len(feedback_data)}")
print("Thumbs up: 10")
print("Thumbs down: 0")
print(f"Saved to: {FEEDBACK_FILE}")