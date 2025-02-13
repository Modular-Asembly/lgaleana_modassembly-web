from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.modassembly.auth.authenticate import authenticate
from app.modassembly.repositories.business.delete_repository import delete_repository

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)

class DeleteRepositoryInput(BaseModel):
    user_id: int
    repo_name: str

class DeleteRepositoryOutput(BaseModel):
    detail: str

@router.delete(
    "/delete",
    response_model=DeleteRepositoryOutput,
    summary="Delete a Repository",
    description=(
        "Deletes a repository from GitHub and from the local database. "
        "This endpoint is secured with OAuth2PasswordBearer via the authenticate dependency "
        "and requires a valid JWT token in the Authorization header. "
        "Pass the user_id and repo_name in the request body."
    ),
)
def delete_repository_endpoint(
    payload: DeleteRepositoryInput, 
    user_info: dict = Depends(authenticate)
) -> DeleteRepositoryOutput:
    """
    Delete Repository Endpoint

    - **user_id**: ID of the user who owns the repository.
    - **repo_name**: The repository name to delete (without username prefix).
    
    Returns a JSON response with the deletion confirmation message.
    """
    deletion_message: str = delete_repository(user_id=payload.user_id, repo_name=payload.repo_name)
    return DeleteRepositoryOutput(detail=deletion_message)
