import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.auth.authenticate_user import authenticate_user
from app.models.User import User
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.services.auth.create_access_token import create_access_token

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
    access_token: str
    token_type: str


ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user_endpoint(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_sql_session)) -> LoginResponse:
    """
    Endpoint to authenticate a user.

    - **username**: The username of the user.
    - **password**: The password of the user.

    Returns a success message and user data if authentication is successful, otherwise returns an error message.
    """
    logger.info("login_user_endpoint called with username: %s", form_data.username)

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.error("Authentication failed for username: %s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.username, access_token_expires)

    response = LoginResponse(
        message="Authentication successful",
        user_id=user.id,
        username=user.username.__str__(),
        email=user.email.__str__(),
        access_token=access_token,
        token_type="bearer"
    )

    logger.info("Authentication successful for username: %s", form_data.username)
    return response
