import os
import logging
from dotenv import load_dotenv
from agent import get_open_prs, get_pr_diff,generate_tests_from_diff,post_pr_comment, already_commented, save_tests_to_file
from config import GITHUB_OWNER, GITHUB_REPO

load_dotenv()

# Configure logging — writes to both terminal and a log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("qa_agent.log")
    ]
)

logger = logging.getLogger(__name__)

def main():
    logger.info("QA Agent starting...")

    owner = GITHUB_OWNER
    repo = GITHUB_REPO

    # Get list of open PRs
    logger.info(f"Fetching open PRs for {owner}/{repo}...")
    prs = get_open_prs(owner, repo)

    if not prs:
        logger.info("No open PRs found.")
        return

    logger.info(f"Found {len(prs)} open PR(s).\n")

    # Process every open PR, not just the first one
    for pr in prs:
        pr_number = pr['number']
        pr_title = pr['title']
        logger.info(f"Processing PR #{pr_number}: {pr_title}")

        # Skip if we already commented on this PR
        if already_commented(owner, repo, pr_number):
            logger.info(f"  Already commented. Skipping.\n")
            continue

        # Fetch the diff
        diff = get_pr_diff(owner, repo, pr_number)
        if not diff:
            logger.warning(f"  Could not fetch diff. Skipping.\n")
            continue

        # Generate tests
        logger.info(f"  Generating tests...")
        tests = generate_tests_from_diff(diff)
        save_tests_to_file(pr_number, tests)
        # Skip if LLM returned nothing
        if not tests:
            logger.warning(f"  No tests generated. Skipping.\n")
            continue

        # Post comment
        logger.info(f"  Posting comment...")
        success = post_pr_comment(owner, repo, pr_number, tests)

        if success:
            logger.info(f"  Done.\n")
        else:
            logger.info(f"  Failed to post comment.\n")





if __name__ == "__main__":
    main()