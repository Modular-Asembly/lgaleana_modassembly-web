import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.services.auth.authenticate_request import authenticate_request
from app.services.github.delete_github_repository import delete_github_repository
from app.services.repository.delete_local_repository import delete_local_repository
from app.models.User import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class DeleteRepositoryRequest(BaseModel):
    repository_id: int
    repository_name: str

class DeleteRepositoryResponse(BaseModel):
    message: str

@router.delete("/repository", response_model=DeleteRepositoryResponse, status_code=status.HTTP_200_OK)
def delete_repository_endpoint(
    delete_request: DeleteRepositoryRequest,
    current_user: User = Depends(authenticate_request)
) -> DeleteRepositoryResponse:
    """
    Endpoint to delete a repository.

    - **repository_id**: The ID of the repository to delete.
    - **repository_name**: The name of the repository to delete.

    Returns a success message if deletion is successful, otherwise returns an error message.
    """
    logger.info("delete_repository_endpoint called with repository_id: %d, repository_name: %s", delete_request.repository_id, delete_request.repository_name)

    # 3) Uses the hardcoded organization name 'Modular-Asembly'.
    org_name = "Modular-Asembly"

    # 4) Calls delete_local_repository to remove the local Repository instance and associated Conversations.
    delete_local_repository(delete_request.repository_id)

    # 5) Calls delete_github_repository to delete the repository on GitHub.
    github_response = delete_github_repository(org_name, delete_request.repository_name)
    if github_response["status_code"] != "204":
        logger.error("Failed to delete GitHub repository: %s", github_response["message"])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete GitHub repository: {github_response['message']}"
        )

    response = DeleteRepositoryResponse(message="Repository deleted successfully")
    logger.info("Repository deleted successfully: %s", delete_request.repository_name)
    return response
