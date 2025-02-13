import os
import requests
from typing import Final

def check_github_repo_exists(user_name: str, repo_name: str) -> bool:
    github_org: Final[str] = os.environ["GITHUB_ORG"]
    token: Final[str] = os.environ["GITHUB_TOKEN"]
    repo_full_name: str = f"{user_name}_{repo_name}"
    url: str = f"https://api.github.com/repos/{github_org}/{repo_full_name}"
    headers: dict[str, str] = {"Authorization": f"token {token}"}
    response: requests.Response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    if response.status_code == 404:
        return False
    response.raise_for_status()
    return False  # This line is unreachable, but satisfies mypy.
