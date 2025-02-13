from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.modassembly.users.business.login_user import login_user

router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

class LoginUserInput(BaseModel):
    email: EmailStr
    plain_password: str

class LoginUserOutput(BaseModel):
    token: str

@router.post(
    "",
    response_model=LoginUserOutput,
    summary="User Login",
    description=(
        "Receives login requests. Validates the input payload and calls the login_user "
        "business logic for authentication. Returns an authentication token if the credentials "
        "are valid, otherwise an HTTP error is raised."
    ),
)
def login_user_endpoint(payload: LoginUserInput) -> LoginUserOutput:
    """
    Endpoint to log in a user.
    
    - **email**: user's email address.
    - **plain_password**: user's plaintext password.
    
    Returns a JSON object with a field `token` containing the authentication token.
    """
    token = login_user(email=payload.email, plain_password=payload.plain_password)
    return LoginUserOutput(token=token)
