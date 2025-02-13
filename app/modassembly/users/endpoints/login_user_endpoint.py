from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.modassembly.users.business.login_user import login_user

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="User Login",
    description="Endpoint to log in a user by validating the input payload and returning an authentication token."
)
def login_user_endpoint(payload: LoginRequest) -> LoginResponse:
    """
    FastAPI endpoint that receives login requests, validates the input payload using pydantic,
    calls the business logic function login_user for authentication, and returns an authentication
    token if login is successful. Raises HTTPException with a 401 status code if authentication fails.
    """
    try:
        token: str = login_user(email=payload.email, plain_password=payload.password)
        return LoginResponse(token=token)
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error))
