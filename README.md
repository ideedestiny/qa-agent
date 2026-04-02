# QA Agent

An agentic Python tool that watches GitHub repositories for new pull requests,

reads the code diff, and automatically generates Pytest test cases using an LLM.

The generated tests are posted directly as a comment on the PR.


## What it does

1\. Connects to the GitHub API and fetches open pull requests

2\. Reads the raw diff for each unprocessed PR

3\. Skips PRs with no Python changes

4\. Sends the diff to GPT-4o-mini with a QA engineering prompt

5\. Generates self-contained, runnable Pytest tests

6\. Posts the tests as a formatted comment on the PR

7\. Tracks which PRs have been processed to avoid duplicates


## Why this exists

In regulated industries and high-velocity engineering teams, every code change

needs test coverage. This agent automates the first layer of that process —

generating a test scaffold before a human reviewer even opens the PR.


## Tech stack

\- Python 3.12

\- GitHub REST API

\- OpenAI API (gpt-4o-mini)

\- Pytest

\- python-dotenv

## Setup

1\. Clone the repo

2\. Create a virtual environment: `uv venv`

3\. Install dependencies: `uv add requests pytest python-dotenv openai`

4\. Copy `.env.example` to `.env` and add your tokens

5\. Run: `python main.py`



\## Project structure



\- `main.py` — orchestrates the pipeline

\- `agent.py` — all GitHub and LLM functions

\- `generated\_tests/` — output directory, not tracked in git



