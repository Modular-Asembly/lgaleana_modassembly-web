from typing import Iterator
from sqlalchemy.orm import Session
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.github.business.delete_github_repository import delete_github_repository
from app.modassembly.models.repository.Repository import Repository
from app.modassembly.models.user.User import User
from app.modassembly.conversations.business.delete_conversations_for_repository import delete_conversations_for_repository

def delete_repository(user_id: int, repo_name: str) -> str:
    session_iter: Iterator[Session] = get_sql_session()
    db: Session = next(session_iter)

    # Retrieve the user to get the username
    user: User | None = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError(f"User with id {user_id} not found")

    # Construct the repository full name from username and repo_name
    full_repo_name: str = f"{user.username}_{repo_name}"

    # Retrieve the repository record
    repo: Repository | None = db.query(Repository).filter(
        Repository.user_id == user_id,
        Repository.name == full_repo_name
    ).first()

    if repo is None:
        raise ValueError(f"Repository '{full_repo_name}' not found for user with id {user_id}")

    # Delete the repository from GitHub
    # This function will raise an error if the repository does not exist on GitHub.
    delete_github_repository(user.username, repo_name)

    # Delete all associated conversations for the repository
    delete_conversations_for_repository(repo.id)

    # Delete the repository record from the local database
    db.delete(repo)
    db.commit()

    try:
        next(session_iter)
    except StopIteration:
        pass

    return "Repository deleted successfully"
