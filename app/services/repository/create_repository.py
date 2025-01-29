import logging
import os
import shutil
from typing import Any

from sqlalchemy.orm import Session

from app.models.Repository import Repository
from app.services.github.check_github_repository_exists import check_github_repository_exists
from app.services.github.create_github_repository import create_github_repository
from app.services.conversation.create_initial_conversations import create_initial_conversations
from app.services.local.execute_git_commands import execute_git_commands
from app.services.github.protect_github_repository import protect_github_repository
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REPOS_DIR = os.path.expanduser("~/repos")
TEMPLATE_DIR = os.path.join(REPOS_DIR, "fastapi-template")

def create_repository(org_name: str, repo_name: str, user_id: int) -> str:
    logger.info("create_repository called with org_name: %s, repo_name: %s, user_id: %d", org_name, repo_name, user_id)

    # 2) Calls check_github_repository_exists to verify if the repository already exists.
    if check_github_repository_exists(org_name, repo_name):
        error_message = f"Repository '{repo_name}' already exists in organization '{org_name}'."
        logger.error(error_message)
        raise ValueError(error_message)

    # 4) Creates a local repository folder and copies a '.gitignore' from the template.
    repo_path = os.path.join(REPOS_DIR, repo_name)
    os.makedirs(repo_path, exist_ok=True)
    shutil.copy(os.path.join(TEMPLATE_DIR, ".gitignore"), repo_path)

    # 5) Calls create_github_repository to create the repository on GitHub and retrieves the GitHub URL.
    github_response = create_github_repository(org_name, repo_name)
    github_url = github_response.get("html_url", "")
    if not github_url:
        error_message = "Failed to retrieve GitHub URL after repository creation."
        logger.error(error_message)
        raise ValueError(error_message)

    # 6) Creates a new Repository instance in the local database with the GitHub URL.
    session: Session = next(get_sql_session())
    new_repository = Repository(
        name=repo_name,
        owner_id=user_id,
        github_url=github_url
    )
    session.add(new_repository)
    session.commit()
    session.refresh(new_repository)
    session.close()

    # 7) Calls create_initial_conversations to create 'brainstorm' and 'architecture' conversations.
    create_initial_conversations(new_repository.id)

    # 8) Executes git commands to initialize the repository and push to GitHub.
    git_commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "Initial commit"],
        ["git", "branch", "-M", "main"],
        ["git", "remote", "add", "origin", f"git@github.com:{org_name}/{repo_name}.git"],
        ["git", "push", "-u", "origin", "main"]
    ]
    execute_git_commands(git_commands, repo=repo_name)

    # 9) Calls protect_github_repository to protect the repository.
    protect_github_repository(org_name, repo_name)

    # 10) Returns a success message.
    success_message = f"Repository '{repo_name}' created successfully in organization '{org_name}'."
    logger.info(success_message)
    return success_message
