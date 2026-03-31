import os
import requests
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env file
load_dotenv()

# Get the GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Headers sent with every GitHub API request

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def get_open_prs(owner, repo):
    # Build the GitHub API URL for listing pull requests
    # owner = the GitHub username or org
    # repo = the repository name
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
    diff_headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=diff_headers)

    # Check if the request failed
    if response.status_code != 200:
        print(f"Error fetching diff: {response.status_code}")
        return None

    # Reject diffs that are too large — protects against token overuse
    if len(response.text) > 10000:
        print("  Diff too large, truncating to 10000 characters.")
        return response.text[:10000]


    # Reject diffs with no meaningful content
    if len(response.text.strip()) < 200:
        print("  Diff too small — likely an empty or non-code change.")
        return None

    # Skip non-Python files — no point generating Pytest tests for markdown
    if ".py" not in response.text:
        print("  No Python files in diff. Skipping.")
        return None

    return response.text

def print_pr_summary(prs):
    # Handle the case where no PRs were found
    if not prs:
        print("No PRs found.")
        return

    # Loop through each PR and print key details
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
    prompt = f"""You are a senior QA engineer reviewing a pull request.

    Analyze this diff and write Pytest tests for the changed code.

    Rules:
    - Only use Python standard library — no external imports except pytest
    - Write self-contained tests that do not import from the changed codebase
    - Test the logic and behaviour described in the diff, not the implementation
    - Use simple assertions — no mocks unless absolutely necessary
    - Each test function must start with test_
    - Return ONLY the Python code. No explanation, no intro text, no markdown backticks.
    - Add one comment per test explaining what it verifies
    - Define any function you are testing directly inside the test file — do not import it

    Diff:
    {diff}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )

        # Extract just the text from the response
        # The response object has nested structure — this navigates to the actual text
        # Strip markdown code blocks if LLM includes them despite instructions
        tests = response.choices[0].message.content

    except Exception as e:
    # Catches any OpenAI API error — rate limits, timeouts, invalid requests
        print(f"  LLM API error: {e}")
        return None

    # Remove any lines before the first 'import' or 'def' — LLM preamble
    tests = tests.replace("```python", "").replace("```", "").strip()
    lines = tests.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("import") or line.startswith("def") or line.startswith("#"):
            tests = "\n".join(lines[i:])
            break

    return tests


def post_pr_comment(owner, repo, pr_number, comment_body):
# This endpoint is for issues/PR comments
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"

    # The body of our POST request
    # We wrap the tests in markdown code blocks so they render nicely
    payload = {
        "body": f"## 🤖 QA Agent — Auto-generated Pytest Tests\n\n```python\n{comment_body}\n```"
    }

    # POST sends data to GitHub
    response = requests.post(url, headers=HEADERS, json=payload)

    # 201 means "created successfully" — different from 200
    if response.status_code == 201:
        print(f"Comment posted successfully!")
        print(f"View it at: {response.json()['html_url']}")
        return True
    else:
        print(f"Error posting comment: {response.status_code} - {response.text}")
        return False

def already_commented(owner, repo, pr_number):
    # Fetch all existing comments on this PR
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return False

    comments = response.json()
    # Check if any existing comment was posted by us and contains our signature
    for comment in comments:
        if "QA Agent" in comment['body']:
            return True

    return False


def save_tests_to_file(pr_number, tests):
    # Create a tests directory if it doesn't exist
    # exist_ok=True means don't throw an error if it already exists
    os.makedirs("generated_tests", exist_ok=True)

    # Name the file after the PR number so it's easy to trace back
    filename = f"generated_tests/test_pr_{pr_number}.py"

    with open(filename, "w") as f:
        f.write(tests)

    print(f"  Tests saved to {filename}")
    return filename


