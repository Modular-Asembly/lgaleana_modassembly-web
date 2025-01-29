import logging
import os
import requests
from typing import Dict

from app.services.github.check_github_repository_exists import check_github_repository_exists

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_github_repository(org_name: str, repo_name: str) -> Dict[str, str]:
    logger.info("create_github_repository called with org_name: %s, repo_name: %s", org_name, repo_name)

    # 2) Calls check_github_repository_exists to verify if the repository already exists
    if check_github_repository_exists(org_name, repo_name):
        logger.error("Repository already exists: %s/%s", org_name, repo_name)
        raise ValueError(f"Repository '{org_name}/{repo_name}' already exists.")

    # 4) Authenticates with the GitHub API using the GITHUB_TOKEN environment variable
    github_token = os.environ["GITHUB_TOKEN"]
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 5) Sends a request to create a new repository on GitHub
    url = f"https://api.github.com/orgs/{org_name}/repos"
    payload = {
        "name": repo_name,
        "private": True  # Example: create a private repository
    }
    response = requests.post(url, json=payload, headers=headers)

    # Log the response status
    logger.info("GitHub API response status: %s", response.status_code)

    # 6) Returns the response from GitHub
    response_data = {
        "status_code": response.status_code.__str__(),
        "message": "Repository created successfully" if response.status_code == 201 else response.json().get("message", "Error creating repository")
    }
    logger.info("create_github_repository response: %s", response_data)
    return response_data
