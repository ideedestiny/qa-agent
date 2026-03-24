import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("QA Agent starting...")
    token = os.getenv("GITHUB_TOKEN")
    if token:
        print("Github token loaded")
    else:
        print("Warning: No Github token found")


if __name__ == "__main__":
    main()