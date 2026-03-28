import os
from dotenv import load_dotenv

from agent import get_open_prs, print_pr_summary

load_dotenv()

def main():
    print("QA Agent starting...")

    owner = "microsoft"
    repo = "vscode"

    print(f"Fetching open PRs for {owner}/{repo}...")
    prs = get_open_prs(owner, repo)
    print_pr_summary(prs)


if __name__ == "__main__":
    main()