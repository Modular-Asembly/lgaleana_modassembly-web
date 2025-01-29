import os
import logging
from sqlalchemy.orm import Session
from app.models.Repository import Repository
from app.services.github.check_github_repository_exists import check_github_repository_exists
from app.services.conversation.create_initial_conversations import create_initial_conversations
from app.services.github.create_github_repository import create_github_repository
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.services.local.execute_git_commands import execute_git_commands
from app.services.github.protect_github_repository import protect_github_repository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


REPOS = os.path.expanduser("~/repos")


def create_repository(org_name: str, repo_name: str, user_id: int) -> str:
    """
    Creates a new repository in the local database and on GitHub.

    Args:
        org_name (str): The name of the organization.
        repo_name (str): The name of the repository.
        user_id (int): The ID of the user who owns the repository.

    Returns:
        str: A success message.
    """
    logger.info("create_repository called with org_name: %s, repo_name: %s, user_id: %d", org_name, repo_name, user_id)

    # 2) Calls check_github_repository_exists to verify if the repository already exists
    if check_github_repository_exists(org_name, repo_name):
        error_message = f"Repository '{repo_name}' already exists in organization '{org_name}'."
        logger.error(error_message)
        raise ValueError(error_message)
    
    # 3) Creates local repository folder and gitignore
    os.mkdir(f"{REPOS}/{repo_name}")
    with open(f"{REPOS}/fastapi-template/.gitignore", "r") as f1, open(
        f"{REPOS}/{repo_name}/.gitignore", "w"
    ) as f2:
        f2.write(f1.read())

    session: Session = next(get_sql_session())
    try:
        # 4) Creates a new Repository instance in the local database
        new_repository = Repository(
            name=repo_name,
            owner_id=user_id
        )
        session.add(new_repository)
        session.commit()
        session.refresh(new_repository)
        logger.info("Created local repository with id: %d", new_repository.id)

        # 5) Calls create_initial_conversations to create 'brainstorm' and 'architecture' conversations
        create_initial_conversations(new_repository.id)

        # 6) Calls create_github_repository to create the repository on GitHub
        create_github_repository(org_name, repo_name)

        # 7) Executes git init commands
        execute_git_commands(
            [
                ["git", "init"],
                ["git", "add", "."],
                ["git", "commit", "-m", "first commit"],
                ["git", "branch", "-M", "main"],
                [
                    "git",
                    "remote",
                    "add",
                    "origin",
                    f"git@github.com:Modular-Asembly/{repo_name}.git",
                ],
                ["git", "push", "-u", "origin", "main"],
            ],
            repo=repo_name,
        )
        
        # 8) Protects the repository
        protect_github_repository(org_name, repo_name)


        # 7) Returns a success message
        success_message = f"Repository '{repo_name}' created successfully in organization '{org_name}'."
        logger.info(success_message)
        return success_message
    finally:
        session.close()
