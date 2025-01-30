import logging
import os
from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.models.User import User
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT configuration
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"

# HTTP Bearer for token extraction
security = HTTPBearer()

def authenticate_request(request: Request) -> User:
    logger.info("authenticate_request called")

    # 1) Extracts and verifies the authentication token from the request headers.
    credentials: Optional[HTTPAuthorizationCredentials] = security(request)
    if credentials is None or credentials.scheme != "Bearer":
        logger.error("Invalid authentication scheme")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )

    token: str = credentials.credentials
    logger.info("Token extracted: %s", token)

    try:
        # 2) Validates the token and retrieves the associated user.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.error("Token payload invalid")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        logger.info("Token payload valid for username: %s", username)

        # Retrieve the user from the database
        session: Session = next(get_sql_session())
        user: Optional[User] = session.query(User).filter(User.username == username).first()
        session.close()

        if user is None:
            logger.error("User not found: %s", username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        logger.info("User authenticated: %s", user.username.__str__())
        return user

    except JWTError as e:
        logger.error("Token validation error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation error",
        )
