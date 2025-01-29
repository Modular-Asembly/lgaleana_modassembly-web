import os
from typing import Any, Dict

import requests


def protect_github_repository(org: str, repo: str) -> Dict[str, Any]:
    owner = "lgaleana"
    token = os.environ["GITHUB_TOKEN"]
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.put(
        f"https://api.github.com/repos/{org}/{repo}/branches/main/protection",
        headers=headers,
        json={
            "required_status_checks": None,
            "enforce_admins": False,
            "required_pull_request_reviews": {
                "dismissal_restrictions": {},
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": False,
                "required_approving_review_count": 1,
                "bypass_pull_request_allowances": {"users": [owner]},
            },
            "restrictions": {"users": [owner], "teams": [], "apps": []},
            "required_linear_history": True,
            "allow_force_pushes": False,
            "allow_deletions": False,
        },
    )
    response.raise_for_status()
    return response.json()
