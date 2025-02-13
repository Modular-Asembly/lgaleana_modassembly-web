from datetime import datetime
from typing import Iterator

from sqlalchemy.orm import Session

from app.modassembly.models.user.User import User
from app.modassembly.users.utils.hash_password import hash_password
from app.modassembly.database.sql.get_sql_session import get_sql_session

def create_user(username: str, email: str, password: str) -> User:
    """
    Creates a new user by validating input, calling hash_password to secure the password,
    and storing the user in the database using get_sql_session.
    """
    hashed = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed,
        created_at=datetime.utcnow()
    )

    session_iter: Iterator[Session] = get_sql_session()
    db: Session = next(session_iter)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    try:
        next(session_iter)
    except StopIteration:
        pass

    return new_user
