import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from app.services.auth.authenticate_request import authenticate_request
from app.services.repository.get_user_repositories import get_user_repositories
from app.models.User import User
from app.models.Repository import Repository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class RepositoryResponse(BaseModel):
    id: int
    name: str
    github_url: str

@router.get("/repositories", response_model=List[RepositoryResponse], status_code=status.HTTP_200_OK)
def get_user_repositories_endpoint(
    user_id: int = Query(..., description="The ID of the user"),
    current_user: User = Depends(authenticate_request)
) -> List[RepositoryResponse]:
    """
    Endpoint to retrieve all repositories associated with a user.

    - **user_id**: The ID of the user.

    Returns a list of repositories or an error message.
    """
    logger.info("get_user_repositories_endpoint called with user_id: %d", user_id)

    if current_user.id != user_id:
        logger.error("Unauthorized access attempt by user_id: %d", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access these repositories."
        )

    repositories = get_user_repositories(user_id)
    response = [
        RepositoryResponse(
            id=repo.id,
            name=repo.name.__str__(),
            github_url=repo.github_url.__str__()
        )
        for repo in repositories
    ]

    logger.info("Retrieved %d repositories for user_id: %d", len(response), user_id)
    return response
