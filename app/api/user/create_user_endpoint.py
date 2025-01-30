import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.auth.authenticate_request import authenticate_request
from app.services.user.create_user import create_user
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.models.User import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str

class CreateUserResponse(BaseModel):
    message: str
    user_id: int
    username: str
    email: str

@router.post("/users", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user_data: CreateUserRequest,
    db: Session = Depends(get_sql_session),
    current_user: User = Depends(authenticate_request)
) -> CreateUserResponse:
    """
    Endpoint to create a new user.

    - **username**: The username of the new user.
    - **email**: The email of the new user.
    - **password**: The password of the new user.

    Returns a success message and user data if creation is successful, otherwise returns an error message.
    """
    logger.info("create_user_endpoint called with username: %s", user_data.username)

    try:
        new_user = create_user(user_data.dict())
        response = CreateUserResponse(
            message="User created successfully",
            user_id=new_user.id,
            username=new_user.username.__str__(),
            email=new_user.email.__str__()
        )
        logger.info("User created successfully with username: %s", new_user.username.__str__())
        return response
    except Exception as e:
        logger.error("Error creating user: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating user"
        )
