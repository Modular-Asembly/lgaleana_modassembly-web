import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

from app.services.github.create_github_repository import create_github_repository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class CreateRepositoryRequest(BaseModel):
    org_name: str
    repo_name: str

class CreateRepositoryResponse(BaseModel):
    status_code: str
    message: str

@router.post("/github/repositories", response_model=CreateRepositoryResponse, summary="Create a GitHub Repository", tags=["GitHub"])
def create_github_repository_endpoint(request: CreateRepositoryRequest) -> CreateRepositoryResponse:
    """
    Create a GitHub repository.

    - **org_name**: The name of the organization.
    - **repo_name**: The name of the repository.
    """
    logger.info("create_github_repository_endpoint called with org_name: %s, repo_name: %s", request.org_name, request.repo_name)

    # 2) Calls the create_github_repository function
    response_data: Dict[str, str] = create_github_repository(request.org_name, request.repo_name)

    # 3) Returns the response from GitHub or an error message
    if response_data["status_code"] != "201":
        logger.error("Error creating repository: %s", response_data["message"])
        raise HTTPException(status_code=int(response_data["status_code"]), detail=response_data["message"])

    logger.info("Repository created successfully: %s", response_data["message"])
    return CreateRepositoryResponse(**response_data)
