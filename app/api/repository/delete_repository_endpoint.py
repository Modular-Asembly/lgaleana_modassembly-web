import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

from app.services.repository.delete_local_repository import delete_local_repository
from app.services.github.delete_github_repository import delete_github_repository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class DeleteRepositoryRequest(BaseModel):
    org_name: str
    repo_name: str
    repository_id: int

class DeleteRepositoryResponse(BaseModel):
    message: str

@router.delete("/repositories", response_model=DeleteRepositoryResponse, summary="Delete a repository", tags=["Repositories"])
def delete_repository_endpoint(request: DeleteRepositoryRequest) -> DeleteRepositoryResponse:
    """
    Deletes a repository both locally and on GitHub.

    - **org_name**: The name of the organization.
    - **repo_name**: The name of the repository.
    - **repository_id**: The ID of the local repository.

    Returns a success message or an error.
    """
    logger.info("delete_repository_endpoint called with org_name: %s, repo_name: %s, repository_id: %d", request.org_name, request.repo_name, request.repository_id)

    # 2) Calls delete_local_repository to remove the local Repository instance and associated Conversations
    delete_local_repository(request.repository_id)
    logger.info("Local repository and conversations deleted for repository_id: %d", request.repository_id)

    # 3) Calls delete_github_repository to delete the repository on GitHub
    response_data: Dict[str, str] = delete_github_repository(request.org_name, request.repo_name)
    if response_data["status_code"] != "204":
        logger.error("Error deleting GitHub repository: %s", response_data["message"])
        raise HTTPException(status_code=int(response_data["status_code"]), detail=response_data["message"])

    logger.info("GitHub repository deleted successfully: %s", response_data["message"])

    # 4) Returns a success message
    return DeleteRepositoryResponse(message="Repository deleted successfully")
