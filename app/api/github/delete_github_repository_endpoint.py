import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.repository.delete_local_repository import delete_local_repository
from app.services.github.delete_github_repository import delete_github_repository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class DeleteRepositoryRequest(BaseModel):
    org_name: str
    repo_name: str

class DeleteRepositoryResponse(BaseModel):
    message: str

@router.delete("/github/repositories", response_model=DeleteRepositoryResponse, summary="Delete a GitHub Repository", tags=["GitHub"])
def delete_github_repository_endpoint(request: DeleteRepositoryRequest) -> DeleteRepositoryResponse:
    """
    Deletes a GitHub repository and its local representation.

    - **org_name**: The name of the organization.
    - **repo_name**: The name of the repository.

    This endpoint performs the following actions:
    1) Calls delete_local_repository to remove the local Repository instance and associated Conversations.
    2) Calls delete_github_repository to delete the repository on GitHub.
    3) Returns a success message or error.
    """
    logger.info("delete_github_repository_endpoint called with org_name: %s, repo_name: %s", request.org_name, request.repo_name)

    try:
        # 2) Calls delete_local_repository
        delete_local_repository(repository_id=int(request.repo_name))  # Assuming repo_name is used as an ID here

        # 3) Calls delete_github_repository
        response_data = delete_github_repository(request.org_name, request.repo_name)

        if response_data["status_code"] != "204":
            logger.error("Error deleting repository: %s", response_data["message"])
            raise HTTPException(status_code=int(response_data["status_code"]), detail=response_data["message"])

        logger.info("Repository deleted successfully: %s", response_data["message"])
        return DeleteRepositoryResponse(message="Repository deleted successfully")
    except Exception as e:
        logger.error("Error in delete_github_repository_endpoint: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
