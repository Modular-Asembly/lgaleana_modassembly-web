import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.services.auth.authenticate_request import authenticate_request
from app.services.repository.create_repository import create_repository
from app.models.User import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class CreateRepositoryRequest(BaseModel):
    repository_name: str

class CreateRepositoryResponse(BaseModel):
    message: str

@router.post("/repositories", response_model=CreateRepositoryResponse, status_code=status.HTTP_201_CREATED)
def create_repository_endpoint(
    request: CreateRepositoryRequest,
    user: User = Depends(authenticate_request)
) -> CreateRepositoryResponse:
    """
    Endpoint to create a new repository.

    - **repository_name**: The name of the repository to create.

    Returns a success message if the repository is created successfully, otherwise returns an error message.
    """
    logger.info("create_repository_endpoint called with repository_name: %s", request.repository_name)

    try:
        # 3) Uses the hardcoded organization name 'Modular-Asembly'.
        org_name = "Modular-Asembly"

        # 4) Calls the create_repository function with the organization name, repository name, and user ID.
        success_message = create_repository(org_name, request.repository_name, user.id)

        response = CreateRepositoryResponse(message=success_message)
        logger.info("Repository created successfully: %s", request.repository_name)
        return response

    except Exception as e:
        logger.error("Error creating repository: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
