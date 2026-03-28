import os
from dotenv import load_dotenv
from agent import get_open_prs, print_pr_summary, get_pr_diff,generate_tests_from_diff

load_dotenv()


def main():
    print("QA Agent starting...")

    owner = "microsoft"
    repo = "vscode"

    # Get list of open PRs
    print(f"Fetching open PRs for {owner}/{repo}...")
    prs = get_open_prs(owner, repo)
    print_pr_summary(prs)

    # Fetch the diff for the first PR in the list
    # grab its number to use in the diff request
    if prs:
        first_pr = prs[0]
        pr_number = first_pr['number']
        pr_title = first_pr['title']

        print(f"\nFetching diff for PR #{pr_number}: {pr_title}")
        diff = get_pr_diff(owner, repo, pr_number)

        if diff:
            # Print only the first 500 characters so it doesn't flood the terminal
            print("\n--- DIFF PREVIEW ---")
            print(diff[:500])
            print("\n--- END PREVIEW ---")

        # Send the diff to the LLM and generate tests
            print("\nGenerating Pytest tests...")
            tests = generate_tests_from_diff(diff)

            print("\n--- GENERATED TESTS ---")
            print(tests)
            print("--- END TESTS ---")


if __name__ == "__main__":
    main()