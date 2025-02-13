from typing import Iterator
from sqlalchemy.orm import Session

from app.modassembly.github.business.create_github_repository import create_github_repository
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.models.repository.Repository import Repository
from app.modassembly.models.user.User import User
from app.modassembly.conversations.business.create_conversations_for_repository import create_conversations_for_repository

def create_repository(user_id: int, repo_name: str) -> Repository:
    session_iter: Iterator[Session] = get_sql_session()
    db: Session = next(session_iter)
    
    # Verify that the user exists
    user: User | None = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError(f"User with id {user_id} not found")
    
    # Construct repository name using user's username and the provided repo_name
    constructed_repo_name: str = f"{user.username}_{repo_name}"
    
    # Check that the repository doesn't already exist in GitHub and create it via GitHub API.
    # If it already exists, create_github_repository will raise a ValueError.
    _ = create_github_repository(user.username, repo_name)
    
    # Create a new Repository record in the local database
    new_repository = Repository(
        name=constructed_repo_name,
        user_id=user.id
    )
    db.add(new_repository)
    db.commit()
    db.refresh(new_repository)
    
    # Create default conversations for the repository
    create_conversations_for_repository(new_repository.id)
    
    try:
        next(session_iter)
    except StopIteration:
        pass
    
    return new_repository
