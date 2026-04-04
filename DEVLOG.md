## Live System Observations

- PRs processed: ~10 (microsoft/vscode run)
- Comments posted: 8
- Reactions received from engineers: yes (merges)
- PRs merged after comment: several
- Comments assessed as relevant: 3-4 (honest estimate)

Notes:
- Most TypeScript PRs skipped correctly — Python filter working
- Large diffs truncated — some context lost, affects test quality
- Best outputs came from small focused diffs (under 200 lines)
- Generic outputs on large truncated diffs — known limitation

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