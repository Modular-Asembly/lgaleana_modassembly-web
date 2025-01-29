import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

from app.services.github.delete_github_repository import delete_github_repository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class DeleteRepositoryRequest(BaseModel):
    org_name: str
    repo_name: str

class DeleteRepositoryResponse(BaseModel):
    status_code: str
    message: str

@router.delete("/github/repositories", response_model=DeleteRepositoryResponse, summary="Delete a GitHub Repository", tags=["GitHub"])
def delete_github_repository_endpoint(request: DeleteRepositoryRequest) -> DeleteRepositoryResponse:
    """
    Delete a GitHub repository.

    - **org_name**: The name of the organization.
    - **repo_name**: The name of the repository.
    """
    logger.info("delete_github_repository_endpoint called with org_name: %s, repo_name: %s", request.org_name, request.repo_name)

    # 2) Calls the delete_github_repository function
    response_data: Dict[str, str] = delete_github_repository(request.org_name, request.repo_name)

    # 3) Returns the response from GitHub or an error message
    if response_data["status_code"] != "204":
        logger.error("Error deleting repository: %s", response_data["message"])
        raise HTTPException(status_code=int(response_data["status_code"]), detail=response_data["message"])

    logger.info("Repository deleted successfully: %s", response_data["message"])
    return DeleteRepositoryResponse(**response_data)
