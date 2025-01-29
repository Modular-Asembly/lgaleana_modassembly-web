import logging
import os
import requests
from requests.auth import HTTPBasicAuth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_github_repository_exists(org_name: str, repo_name: str) -> bool:
    """
    Checks if a GitHub repository exists under the specified organization.

    Args:
        org_name (str): The name of the organization.
        repo_name (str): The name of the repository.

    Returns:
        bool: True if the repository exists, otherwise False.
    """
    logger.info("check_github_repository_exists called with org_name: %s, repo_name: %s", org_name, repo_name)

    # 2) Authenticates with the GitHub API using the GITHUB_TOKEN environment variable
    github_token = os.environ["GITHUB_TOKEN"]

    # 3) Sends a request to check if the repository exists
    url = f"https://api.github.com/repos/{org_name}/{repo_name}"
    response = requests.get(url, auth=HTTPBasicAuth('username', github_token))  # 'username' can be any string

    # 4) Returns True if the repository exists, otherwise False
    exists = response.status_code == 200
    logger.info("Repository exists: %s", exists)
    return exists
