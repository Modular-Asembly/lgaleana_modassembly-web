from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.modassembly.auth.authenticate import authenticate
from app.modassembly.models.repository.Repository import Repository
from app.modassembly.repositories.business.create_repository import create_repository

router: APIRouter = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
    responses={404: {"description": "Not found"}},
)

class CreateRepositoryInput(BaseModel):
    repo_name: str = Field(..., description="The name of the repository to create.")

class CreateRepositoryOutput(BaseModel):
    id: int = Field(..., description="The repository ID.")
    name: str = Field(..., description="The full constructed repository name.")
    user_id: int = Field(..., description="ID of the owner user.")

@router.post(
    "/create",
    response_model=CreateRepositoryOutput,
    summary="Create a new repository",
    description=(
        "Creates a new repository for the authenticated user. "
        "Validates the payload, calls the repository creation business logic, "
        "and returns repository details upon successful creation."
    ),
)
def create_repository_endpoint(
    payload: CreateRepositoryInput,
    user: Dict[str, Any] = Depends(authenticate),
) -> CreateRepositoryOutput:
    """
    Endpoint to create a new repository.

    - **repo_name**: The desired repository name.
    - The authenticated user's ID is extracted from the JWT token payload.
    """
    try:
        user_id: int = int(user["user_id"])
    except (KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token payload",
        ) from exc

    repository: Repository = create_repository(user_id=user_id, repo_name=payload.repo_name)
    return CreateRepositoryOutput(
        id=repository.id,
        name=repository.name,
        user_id=repository.user_id,
    )
