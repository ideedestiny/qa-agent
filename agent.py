import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
# This makes GITHUB_TOKEN available to os.getenv()
load_dotenv()

# Get the GitHub token from environment variables
# Never hardcode tokens directly in code
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Headers sent with every GitHub API request
# Authorization proves who we are
# Accept tells GitHub we want JSON back
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def get_open_prs(owner, repo):
    # Build the GitHub API URL for listing pull requests
    # owner = the GitHub username or org (e.g. "microsoft")
    # repo = the repository name (e.g. "vscode")
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    # Make the GET request to GitHub
    response = requests.get(url, headers=HEADERS)

    # Check if the request failed
    # 200 means success, anything else is an error
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return []

    # Convert the response from raw text to a Python list of dictionaries
    # Each dictionary represents one pull request
    prs = response.json()
    return prs


def print_pr_summary(prs):
    # Handle the case where no PRs were found
    if not prs:
        print("No PRs found.")
        return

    # Loop through each PR and print key details
    # pr is a dictionary — pr['number'], pr['title'] etc are its keys
    for pr in prs:
        print(f"PR #{pr['number']}: {pr['title']}")
        print(f"  Author: {pr['user']['login']}")
        print(f"  URL: {pr['html_url']}")
        print()