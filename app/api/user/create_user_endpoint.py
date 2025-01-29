import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.user.create_user import create_user
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str

class UserCreateResponse(BaseModel):
    id: int
    username: str
    email: str
    message: str

@router.post("/users", response_model=UserCreateResponse, summary="Create a new user", tags=["Users"])
def create_user_endpoint(user_data: UserCreateRequest, db: Session = Depends(get_sql_session)) -> UserCreateResponse:
    """
    Create a new user.

    - **username**: The username of the user.
    - **email**: The email address of the user.
    - **password**: The password of the user.
    """
    logger.info("create_user_endpoint called with user_data: %s", user_data)

    try:
        new_user = create_user(user_data.dict())
        response = UserCreateResponse(
            id=new_user.id,
            username=new_user.username.__str__(),
            email=new_user.email.__str__(),
            message="User created successfully"
        )
        logger.info("User created successfully with id: %s", new_user.id.__str__())
        return response
    except Exception as e:
        logger.error("Error creating user: %s", str(e))
        raise HTTPException(status_code=400, detail="Error creating user")
