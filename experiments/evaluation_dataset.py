EVALUATION_DATASET = [
    {
        "question": "What is the status of order TN1001?",
        "reference": "TN1001 is a Laptop Pro 14. Its status is Shipped and the ETA is 2 days."
    },
    {
        "question": "What item is in order TN1002?",
        "reference": "TN1002 contains Noise-cancel Earbuds."
    },
    {
        "question": "What is the status of order TN1003?",
        "reference": "TN1003 is a Phone X. Its status is Delivered."
    },
    {
        "question": "What is TechNova's return policy?",
        "reference": "Returns are accepted within 30 days in the original packaging."
    },
    {
        "question": "What is TechNova's warranty policy?",
        "reference": "Electronics come with a 1-year manufacturer warranty."
    },
    {
        "question": "What is TechNova's shipping policy?",
        "reference": "Free shipping is available for orders above Rs.999. Standard delivery takes 3-5 days."
    },
    {
        "question": "How long do I have to return a product?",
        "reference": "Products can be returned within 30 days."
    },
    {
        "question": "Does TechNova provide a warranty for electronics?",
        "reference": "Yes. Electronics come with a 1-year manufacturer warranty."
    },
    {
        "question": "Is shipping free for orders above Rs.999?",
        "reference": "Yes. TechNova provides free shipping for orders above Rs.999."
    },
    {
        "question": "What item was ordered in TN1001?",
        "reference": "The item in order TN1001 is a Laptop Pro 14."
    }
]


if __name__ == "__main__":
    print(f"Total evaluation questions: {len(EVALUATION_DATASET)}")

    for i, item in enumerate(EVALUATION_DATASET, start=1):
        print(f"\n{i}. {item['question']}")
        print(f"   Reference: {item['reference']}")