from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from app.modassembly.auth.authenticate import authenticate
from app.modassembly.models.user.User import User  # SQLAlchemy model
from app.modassembly.users.business.create_user import create_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


class CreateUserInput(BaseModel):
    username: str = Field(..., title="Username", description="Unique username for the user")
    email: EmailStr = Field(..., title="Email", description="User's email address")
    password: str = Field(..., title="Password", description="User's plaintext password")


class CreateUserOutput(BaseModel):
    id: int = Field(..., title="User ID", description="The unique identifier of the created user")
    username: str = Field(..., title="Username", description="Unique username for the user")
    email: EmailStr = Field(..., title="Email", description="User's email address")
    created_at: datetime = Field(..., title="Creation Time", description="Timestamp when the user was created")


@router.post(
    "/create",
    response_model=CreateUserOutput,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New User",
    description=(
        "Creates a new user by accepting username, email, and password. "
        "Requires authentication via OAuth2PasswordBearer. Returns the details of the newly created user."
    ),
)
def create_user_endpoint(
    payload: CreateUserInput,
    token_payload: Dict[str, Any] = Depends(authenticate),
) -> CreateUserOutput:
    """
    Create User Endpoint

    This endpoint creates a new user after validating the 
    provided data and ensuring the request is authenticated.

    - **username**: Unique username for the user.
    - **email**: User's email address.
    - **password**: Plaintext password which will be hashed.
    
    Returns the newly created user's details.
    """
    # Call business logic to create the user
    new_user: User = create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
    )
    
    # Construct output; assuming the User model has id, username, email, and created_at attributes.
    return CreateUserOutput(
        id=new_user.id, 
        username=new_user.username, 
        email=new_user.email, 
        created_at=new_user.created_at
    )
