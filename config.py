# Central configuration for the QA Agent
# Change these values to point the agent at a different repo

# Target repository
GITHUB_OWNER = "ideedestiny"
GITHUB_REPO = "qa-agent-test"

# LLM settings
LLM_MODEL = "gpt-4o-mini"
LLM_MAX_TOKENS = 1000

# Diff size limits
MAX_DIFF_SIZE = 10000
MIN_DIFF_SIZE = 200