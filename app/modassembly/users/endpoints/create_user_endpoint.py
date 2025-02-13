from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.modassembly.users.business.create_user import create_user
from app.modassembly.models.user.User import User  # type: ignore

router = APIRouter()

class CreateUserPayload(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: str

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Endpoint to create a new user. Expects a JSON payload with username, email, and password."
)
def create_user_endpoint(payload: CreateUserPayload) -> UserResponse:
    """
    FastAPI endpoint that receives user creation requests, extracts the payload,
    and calls create_user business logic. Returns appropriate HTTP responses.
    """
    try:
        user: User = create_user(payload.username, payload.email, payload.password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at.isoformat()
    )
