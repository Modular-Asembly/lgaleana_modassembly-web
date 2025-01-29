import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.repository.create_repository import create_repository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class CreateRepositoryRequest(BaseModel):
    repo_name: str
    user_id: int

class CreateRepositoryResponse(BaseModel):
    message: str


ORG = "Modular-Asembly"


@router.post("/repositories", response_model=CreateRepositoryResponse, summary="Create a new repository", tags=["Repositories"])
def create_repository_endpoint(request: CreateRepositoryRequest) -> CreateRepositoryResponse:
    """
    Creates a new repository both locally and on GitHub.

    - **org_name**: The name of the organization.
    - **repo_name**: The name of the repository.
    - **user_id**: The ID of the user who owns the repository.

    Returns a success message or an error.
    """
    logger.info("create_repository_endpoint called with org_name: %s, repo_name: %s, user_id: %d", ORG, request.repo_name, request.user_id)

    try:
        # 2) Calls the create_repository function
        success_message = create_repository(ORG, request.repo_name, request.user_id)
        logger.info("Repository created successfully: %s", success_message)

        # 3) Returns a success message
        return CreateRepositoryResponse(message=success_message)
    except ValueError as e:
        logger.error("Error in create_repository_endpoint: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error in create_repository_endpoint: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
