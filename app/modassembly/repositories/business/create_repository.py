from datetime import datetime
from typing import Iterator

from sqlalchemy.orm import Session

from app.modassembly.models.repository.Repository import Repository
from app.modassembly.models.user.User import User
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.github.business.create_github_repository import create_github_repository

def create_repository(user_id: int, repo_name: str) -> Repository:
    session_iter: Iterator[Session] = get_sql_session()
    db: Session = next(session_iter)
    
    user: User | None = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError("User not found")
    
    full_repo_name: str = f"{user.username}_{repo_name}"
    
    # Create the GitHub repository (this will raise if exists)
    github_url: str = create_github_repository(user.username, repo_name)
    
    new_repository: Repository = Repository(
        name=full_repo_name,
        created_at=datetime.utcnow(),
        user_id=user.id
    )
    db.add(new_repository)
    db.commit()
    db.refresh(new_repository)
    
    # Close the database session
    try:
        next(session_iter)
    except StopIteration:
        pass
    
    return new_repository
