import os
import requests
from typing import Final

from app.modassembly.github.utils.check_github_repo_exists import check_github_repo_exists

def create_github_repository(user_name: str, repo_name: str) -> str:
    github_org: Final[str] = os.environ["GITHUB_ORG"]
    token: Final[str] = os.environ["GITHUB_TOKEN"]
    repo_full_name: str = f"{user_name}_{repo_name}"
    
    # Check if repository already exists
    if check_github_repo_exists(user_name, repo_name):
        raise ValueError(f"Repository {repo_full_name} already exists in organization {github_org}")
    
    url: str = f"https://api.github.com/orgs/{github_org}/repos"
    headers: dict[str, str] = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    payload: dict[str, object] = {
        "name": repo_full_name,
        "private": False
    }
    
    response: requests.Response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    repo_data: dict[str, object] = response.json()
    github_url: str = repo_data["html_url"]  # type: ignore
    return github_url
