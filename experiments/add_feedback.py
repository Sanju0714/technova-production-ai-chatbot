from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

PROJECT_NAME = "technova-bot-sanjana"


def main():

    print("\n" + "=" * 70)
    print("ADDING LANGSMITH USER RATINGS")
    print("=" * 70)

    # Use the LangSmith API supported by the installed SDK.
    runs = list(
        client.list_runs(
            project_name=PROJECT_NAME,
            limit=20
        )
    )

    # Keep only LLM runs
    llm_runs = [
        run
        for run in runs
        if run.run_type == "llm"
    ]

    print(f"Found {len(llm_runs)} recent LLM runs.")

    added = 0

    for run in llm_runs:

        if added >= 5:
            break

        try:

            client.create_feedback(
                run.id,
                key="user_rating",
                score=1,
                comment="👍 Correct and helpful answer.",
                session_id=run.session_id
            )

            print(
                f"Added 👍 user_rating to run: {run.id}"
            )

            added += 1

        except Exception as error:

            print(
                f"Could not add feedback to "
                f"{run.id}: {error}"
            )

    print("\n" + "=" * 70)
    print(f"USER RATINGS ADDED: {added}")
    print("=" * 70)


if __name__ == "__main__":
    main()