import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_open_prs(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"error: {response.status_code}-{response.text}")
        return []

    prs = response.json()
    print(type(prs))
    print(prs)
    return prs

def print_pr_summary(prs):
    if not prs:
        print("No prs found")
        return

    for pr in prs:
        print(f"PR #{pr['number']}: {pr['title']}")
        print(f" Author: {pr['user']['login']}")
        print(f" URL: {pr['html_url']}")
        print()
