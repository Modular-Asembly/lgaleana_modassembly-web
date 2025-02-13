import os
import requests
from typing import Final

from app.modassembly.github.utils.check_github_repo_exists import check_github_repo_exists

def delete_github_repository(user_name: str, repo_name: str) -> str:
    """
    Deletes a repository from the GitHub organization 'Modular-Asembly'. 
    It retrieves the authentication token from the environment variable GITHUB_TOKEN, 
    constructs the repository name as '{user_name}_{repo_name}', and calls the GitHub API 
    to delete the repository if it exists.
    
    Parameters:
        user_name (str): The GitHub username.
        repo_name (str): The repository name (without prefix).
    
    Returns:
        str: A message indicating successful deletion.
    
    Raises:
        ValueError: If the repository does not exist in the GitHub organization.
        requests.HTTPError: For any HTTP-related error returned by the GitHub API.
        KeyError: If required environment variables are missing.
    """
    github_org: Final[str] = os.environ["GITHUB_ORG"]
    token: Final[str] = os.environ["GITHUB_TOKEN"]
    repo_full_name: str = f"{user_name}_{repo_name}"
    
    if not check_github_repo_exists(user_name, repo_name):
        raise ValueError(
            f"Repository {repo_full_name} does not exist in organization {github_org}"
        )
    
    url: str = f"https://api.github.com/repos/{github_org}/{repo_full_name}"
    headers: dict[str, str] = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    
    response: requests.Response = requests.delete(url, headers=headers)
    response.raise_for_status()
    
    return "Repository deleted successfully"
