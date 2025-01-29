import logging
from typing import Optional
from sqlalchemy.orm import Session
import bcrypt
from app.models.User import User
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    logger.info("authenticate_user called with username: %s", username)

    # Retrieve the user from the database
    user: Optional[User] = db.query(User).filter(User.username == username).first()

    if user is None:
        logger.info("User not found: %s", username)
        return None

    # Verify the password
    if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.__str__().encode('utf-8')):
        logger.info("Authentication successful for user: %s", username)
        return user

    logger.info("Authentication failed for user: %s", username)
    return None
