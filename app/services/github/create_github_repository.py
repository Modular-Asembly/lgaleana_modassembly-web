import logging
import os
from typing import Dict, Any

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_github_repository(org_name: str, repo_name: str) -> Dict[str, Any]:
    """
    Creates a new GitHub repository under the specified organization.

    Args:
        org_name (str): The name of the organization.
        repo_name (str): The name of the repository.

    Returns:
        Dict[str, Any]: The response from GitHub.
    """
    logger.info("create_github_repository called with org_name: %s, repo_name: %s", org_name, repo_name)

    # 2) Authenticates with the GitHub API using the GITHUB_TOKEN environment variable
    github_token = os.environ["GITHUB_TOKEN"]
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 3) Sends a POST request to create a new repository on GitHub
    url = f"https://api.github.com/orgs/{org_name}/repos"
    payload = {
        "name": repo_name,
    }
    response = requests.post(url, headers=headers, json=payload)

    # Log the response status
    logger.info("GitHub API response status: %s", response.status_code)

    # 4) Returns the response from GitHub
    response_data = response.json()
    logger.info("create_github_repository response: %s", response_data)
    return response_data
