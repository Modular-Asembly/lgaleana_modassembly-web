import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.auth.authenticate_user import authenticate_user
from app.models.User import User
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: int
    username: str
    email: str

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user_endpoint(login_request: LoginRequest, db: Session = Depends(get_sql_session)) -> LoginResponse:
    """
    Endpoint to authenticate a user.

    - **username**: The username of the user.
    - **password**: The password of the user.

    Returns a success message and user data if authentication is successful, otherwise returns an error message.
    """
    logger.info("login_user_endpoint called with username: %s", login_request.username)

    user = authenticate_user(db, login_request.username, login_request.password)
    if not user:
        logger.error("Authentication failed for username: %s", login_request.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    response = LoginResponse(
        message="Authentication successful",
        user_id=user.id,
        username=user.username.__str__(),
        email=user.email.__str__()
    )

    logger.info("Authentication successful for username: %s", login_request.username)
    return response
