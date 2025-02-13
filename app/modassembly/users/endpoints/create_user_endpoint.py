from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, EmailStr
from app.modassembly.auth.authenticate import authenticate
from app.modassembly.users.business.create_user import create_user
from app.modassembly.models.user.User import User
from datetime import datetime

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

class CreateUserInput(BaseModel):
    username: str
    email: EmailStr
    password: str

class CreateUserOutput(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

@router.post(
    "/create",
    response_model=CreateUserOutput,
    summary="Create a new user",
    description=(
        "Receives a user creation request along with an authentication token. "
        "It authenticates the caller using the JWT token from the Authorization header, "
        "extracts the payload, and calls the create_user business logic to create a new user. "
        "Returns the created user details."
    ),
)
def create_user_endpoint(
    payload: CreateUserInput, authorization: str = Header(...)
) -> CreateUserOutput:
    """
    Endpoint to create a new user.
    
    Expects:
    - **Authorization** header with a Bearer token.
    - JSON payload with `username`, `email`, and `password`.
    
    Returns a JSON object with user details:
    - **id**: User's unique identifier.
    - **username**: The username provided.
    - **email**: The email address provided.
    - **created_at**: Timestamp of user creation.
    """
    # Extract the token from the "Bearer <token>" format.
    try:
        scheme, token = authorization.split()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid authorization header format")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=400, detail="Authorization scheme must be Bearer")
    
    # Authenticate the caller. If the token is invalid, an exception will be raised.
    _ = authenticate(token)
    
    # Create the user using business logic.
    user: User = create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password
    )
    
    return CreateUserOutput(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at
    )
