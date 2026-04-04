# QA Agent — Dev Log

## Week 3 (Mar 31 – Apr 4)
- Replaced all print statements with logging module across agent.py and main.py
- Added timestamps and persistent log file (qa_agent.log)
- Centralized configuration into config.py
- Ran agent against microsoft/vscode — comments posted on live PRs, reactions from engineers
- Wrote 6 unit tests for agent.py using mocking (patch, MagicMock)

## Week 2 (Mar 24 – Mar 30)
- Built duplicate comment detection with already_commented()
- Added loop to process all open PRs, not just the first
- Improved prompt — generated tests now pass pytest locally
- Added error handling for empty diffs, non-Python files, LLM failures
- Saved generated tests to file per PR
- Pushed project to public GitHub repo

## Week 1 (Mar 17 – Mar 24)
- Set up Python environment with uv on Windows
- Connected to GitHub API — fetching live PRs
- Fetched raw diffs using correct Accept header
- Sent diff to gpt-4o-mini, generated Pytest test cases
- Posted generated tests as formatted PR comment
- Full pipeline working end to end