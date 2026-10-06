import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"

llm = ChatOpenAI(
    model=MODEL,
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0,
    max_tokens=256,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    }
)


def ask_with_validation(question):
    if not question or not question.strip():
        print("Invalid user input detected.")
        return "Please enter a question so I can help you."

    try:
        response = llm.invoke(question)
        return response.content

    except Exception:
        return "Sorry, I couldn't process your request right now. Please try again later."


def run_error_rate_test():

    test_cases = [
        "What is the return policy?",
        "",
        "What is the warranty policy?",
        "   ",
        "How long does shipping take?",
        "What is the status of order TN1001?",
        "",
        "Can I return an electronic product?",
        "   ",
        "Does TechNova provide a warranty?"
    ]

    total_requests = len(test_cases)
    successful_requests = 0
    failed_requests = 0

    print("\n" + "=" * 60)
    print("ERROR RATE TEST")
    print("=" * 60)

    for i, question in enumerate(test_cases, start=1):

        print(f"\nRequest {i}: {repr(question)}")

        if not question or not question.strip():
            failed_requests += 1
            print("Result: FAILED - Invalid input")
            continue

        try:
            response = llm.invoke(question)

            if response and response.content:
                successful_requests += 1
                print("Result: SUCCESS")
            else:
                failed_requests += 1
                print("Result: FAILED - Empty response")

        except Exception as e:
            failed_requests += 1
            print(f"Result: FAILED - {type(e).__name__}")

    error_rate = (failed_requests / total_requests) * 100

    print("\n" + "=" * 60)
    print("ERROR RATE RESULTS")
    print("=" * 60)

    print(f"Total requests:      {total_requests}")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests:     {failed_requests}")
    print(f"Error rate:          {error_rate:.2f}%")

    return {
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "error_rate": error_rate
    }


if __name__ == "__main__":
    run_error_rate_test()