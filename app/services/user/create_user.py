import logging
from typing import Dict

import bcrypt
from sqlalchemy.orm import Session

from app.models.User import User
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_user(user_data: Dict[str, str]) -> User:
    logger.info("create_user called with user_data: %s", user_data)

    # 1) Accepts user data as input
    username: str = user_data["username"]
    email: str = user_data["email"]
    password: str = user_data["password"]

    # 2) Hashes the user's password
    password_hash: bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # 3) Creates a new User instance
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash.decode('utf-8')
    )

    # 4) Saves the User instance to the database
    session: Session = next(get_sql_session())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    session.close()

    logger.info("User created with id: %s", new_user.id.__str__())
    return new_user
