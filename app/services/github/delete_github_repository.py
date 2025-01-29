import logging
import os
import requests
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_github_repository(org_name: str, repo_name: str) -> Dict[str, str]:
    logger.info("delete_github_repository called with org_name: %s, repo_name: %s", org_name, repo_name)

    # 2) Authenticates with the GitHub API using the GITHUB_TOKEN environment variable
    github_token = os.environ["GITHUB_TOKEN"]
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 3) Sends a request to delete the specified repository under the organization on GitHub
    url = f"https://api.github.com/repos/{org_name}/{repo_name}"
    response = requests.delete(url, headers=headers)

    # Log the response status
    logger.info("GitHub API response status: %s", response.status_code)

    # 4) Returns the response from GitHub
    response_data = {
        "status_code": response.status_code.__str__(),
        "message": "Repository deleted successfully" if response.status_code == 204 else response.json().get("message", "Error deleting repository")
    }
    logger.info("delete_github_repository response: %s", response_data)
    return response_data
