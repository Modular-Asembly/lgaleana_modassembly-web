from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.modassembly.repositories.business.delete_repository import delete_repository

router = APIRouter()

class DeleteRepositoryPayload(BaseModel):
    user_id: int
    repo_name: str

class DeleteRepositoryResponse(BaseModel):
    message: str

@router.delete(
    "/repositories",
    response_model=DeleteRepositoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Repository",
    description=(
        "Deletes a repository for a given user. The endpoint validates the request payload, "
        "calls the business logic function to delete the repository from GitHub and the local database, "
        "and returns a confirmation message upon successful deletion."
    )
)
def delete_repository_endpoint(payload: DeleteRepositoryPayload) -> DeleteRepositoryResponse:
    """
    FastAPI endpoint that receives repository deletion requests.
    
    Parameters:
        payload (DeleteRepositoryPayload): The payload containing the user_id and the repository name.
    
    Returns:
        DeleteRepositoryResponse: A response containing a message indicating the outcome of the deletion.
    
    Raises:
        HTTPException: If deletion fails due to validation or processing errors.
    """
    message: str = delete_repository(payload.user_id, payload.repo_name)
    return DeleteRepositoryResponse(message=message)
