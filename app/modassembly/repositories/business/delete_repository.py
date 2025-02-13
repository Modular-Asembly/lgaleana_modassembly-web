from typing import Iterator

from sqlalchemy.orm import Session
from app.modassembly.github.business.delete_github_repository import delete_github_repository
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.models.repository.Repository import Repository
from app.modassembly.models.user.User import User

def delete_repository(user_id: int, repo_name: str) -> str:
    """
    Deletes a repository for a given user. The function validates the input, checks if the repository exists
    in the local database, calls delete_github_repository to remove it from GitHub, and then deletes the 
    repository record from the local database using get_sql_session.
    
    Parameters:
        user_id (int): The ID of the user owning the repository.
        repo_name (str): The base repository name (without the user prefix).
        
    Returns:
        str: A message indicating that the repository was deleted.
    
    Raises:
        ValueError: If the user or repository is not found.
        requests.HTTPError: If there's an HTTP error during deletion from GitHub.
        KeyError: If required environment variables are missing.
    """
    session_iter: Iterator[Session] = get_sql_session()
    db: Session = next(session_iter)
    
    # Fetch the User to get the username needed to construct full repository name.
    user: User | None = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError(f"User with id {user_id} not found")
    
    # Construct the full repository name as stored in the database.
    full_repo_name: str = f"{user.username}_{repo_name}"
    
    # Find the repository record in the local database.
    repository: Repository | None = (
        db.query(Repository)
        .filter(Repository.user_id == user_id, Repository.name == full_repo_name)
        .first()
    )
    if repository is None:
        raise ValueError(f"Repository '{full_repo_name}' not found for user with id {user_id}")
    
    # Delete repository from GitHub.
    delete_github_repository(user.username, repo_name)
    
    # Delete repository record from the local database.
    db.delete(repository)
    db.commit()
    
    try:
        next(session_iter)
    except StopIteration:
        pass
    
    return "Repository deleted successfully"
