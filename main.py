import os
from dotenv import load_dotenv
from agent import get_open_prs, print_pr_summary, get_pr_diff,generate_tests_from_diff,post_pr_comment, already_commented, save_tests_to_file

load_dotenv()


def main():
    print("QA Agent starting...")

    owner = "ideedestiny"
    repo = "qa-agent-test"

    # Get list of open PRs
    print(f"Fetching open PRs for {owner}/{repo}...")
    prs = get_open_prs(owner, repo)

    if not prs:
        print("No open PRs found.")
        return

    print(f"Found {len(prs)} open PR(s).\n")

    # Process every open PR, not just the first one
    for pr in prs:
        pr_number = pr['number']
        pr_title = pr['title']
        print(f"Processing PR #{pr_number}: {pr_title}")

        # Skip if we already commented on this PR
        if already_commented(owner, repo, pr_number):
            print(f"  Already commented. Skipping.\n")
            continue

        # Fetch the diff
        diff = get_pr_diff(owner, repo, pr_number)
        if not diff:
            print(f"  Could not fetch diff. Skipping.\n")
            continue

        # Generate tests
        print(f"  Generating tests...")
        tests = generate_tests_from_diff(diff)
        save_tests_to_file(pr_number, tests)
        # Skip if LLM returned nothing
        if not tests:
            print(f"  No tests generated. Skipping.\n")
            continue

        # Post comment
        print(f"  Posting comment...")
        success = post_pr_comment(owner, repo, pr_number, tests)

        if success:
            print(f"  Done.\n")
        else:
            print(f"  Failed to post comment.\n")





if __name__ == "__main__":
    main()