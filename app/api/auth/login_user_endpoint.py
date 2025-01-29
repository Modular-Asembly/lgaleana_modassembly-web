import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.auth.authenticate_user import authenticate_user
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.models.User import User

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

@router.post("/login", response_model=LoginResponse, summary="User Login", description="Authenticate a user with username and password.")
def login_user_endpoint(login_request: LoginRequest, db: Session = Depends(get_sql_session)) -> LoginResponse:
    logger.info("login_user_endpoint called with username: %s", login_request.username)

    user: Optional[User] = authenticate_user(db, login_request.username, login_request.password)

    if user is None:
        logger.info("Authentication failed for username: %s", login_request.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    logger.info("Authentication successful for username: %s", login_request.username)
    return LoginResponse(
        message="Login successful",
        user_id=user.id,
        username=user.username.__str__(),
        email=user.email.__str__()
    )
