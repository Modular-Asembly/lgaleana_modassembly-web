from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.modassembly.auth.authenticate import authenticate
from app.modassembly.repositories.business.create_repository import create_repository
from app.modassembly.models.repository.Repository import Repository

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
    responses={401: {"description": "Unauthorized"}, 404: {"description": "Not found"}},
)

class CreateRepositoryInput(BaseModel):
    repo_name: str

class CreateRepositoryOutput(BaseModel):
    id: int
    name: str
    user_id: int

@router.post(
    "",
    response_model=CreateRepositoryOutput,
    summary="Create Repository",
    description=(
        "Receives repository creation requests, authenticates the user using a Bearer token "
        "provided in the Authorization header, validates the payload, calls the create_repository "
        "business logic, and returns the created repository details."
    ),
)
def create_repository_endpoint(
    payload: CreateRepositoryInput,
    authorization: str = Header(..., description="Bearer token for authentication"),
) -> CreateRepositoryOutput:
    """
    Endpoint to create a new repository for the authenticated user.
    
    - **repo_name**: Name of the repository to be created.
    
    The Authorization header must be in the format: 'Bearer <token>'.
    
    Returns a JSON object with the repository id, name, and associated user_id.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = authorization[7:]  # Remove 'Bearer ' prefix
    auth_payload = authenticate(token)
    
    # Expecting the authentication payload to include the user_id.
    user_id: int = auth_payload["user_id"]
    
    repository: Repository = create_repository(user_id=user_id, repo_name=payload.repo_name)
    
    return CreateRepositoryOutput(
        id=repository.id,
        name=repository.name,
        user_id=repository.user_id,
    )
