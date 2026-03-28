import os
import requests
from dotenv import load_dotenv
from openai import OpenAI


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


def get_pr_diff(owner, repo, pr_number):
    # GitHub requires a special Accept header to get the raw diff format
    # Without this header GitHub returns JSON instead of the actual diff text

    diff_headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    # Build the URL for a specific PR using its number
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"

    # Make the request
    response = requests.get(url, headers=diff_headers)

# Check if the request failed
    if response.status_code != 200:
        print(f"Error fetching diff: {response.status_code}")
        return None

        # Return the raw diff text
        # This is plain text, not JSON, so we use .text not .json()
    return response.text


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


def generate_tests_from_diff(diff):
    # Initialize the OpenAI client
    # It automatically reads OPENAI_API_KEY from your environment
    client = OpenAI()
    # This is the prompt — instructions we give the LLM
    # We tell it exactly what role to play and what to produce
    prompt = f"""You are a senior QA engineer. 
    A developer has submitted the following code diff for review.
    Your job is to write Pytest test cases that verify the changed code works correctly.

    Rules:
    - Write only Pytest test functions
    - Each test must have a clear name describing what it tests
    - Add a one line comment above each test explaining why it matters
    - Do not explain anything, just write the tests

    Here is the diff:
    {diff}
    """
    # Send the prompt to the LLM and get a response
    # model: which AI model to use
    # messages: the conversation — "user" is us, "assistant" will be the LLM
    # max_tokens: maximum length of the response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    # Extract just the text from the response
    # The response object has nested structure — this navigates to the actual text
    return response.choices[0].message.content