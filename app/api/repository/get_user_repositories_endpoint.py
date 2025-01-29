import logging
from typing import List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.services.repository.get_user_repositories import get_user_repositories
from app.models.Repository import Repository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class RepositoryResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    github_url: str
    created_at: str

@router.get("/repositories", response_model=List[RepositoryResponse], summary="Get User Repositories", tags=["Repositories"])
def get_user_repositories_endpoint(user_id: int = Query(..., description="The ID of the user")) -> List[RepositoryResponse]:
    """
    Retrieves all repositories associated with the given user ID.

    - **user_id**: The ID of the user.

    Returns a list of repositories or an error message.
    """
    logger.info("get_user_repositories_endpoint called with user_id: %d", user_id)

    try:
        # 2) Calls the get_user_repositories function
        repositories = get_user_repositories(user_id)
        logger.info("Retrieved %d repositories for user_id: %d", len(repositories), user_id)

        # 3) Returns a list of repositories
        return [
            RepositoryResponse(
                id=repo.id,
                name=repo.name.__str__(),
                owner_id=repo.owner_id,
                github_url=repo.github_url.__str__(),
                created_at=repo.created_at.isoformat()
            )
            for repo in repositories
        ]
    except Exception as e:
        logger.error("Error retrieving repositories for user_id: %d, error: %s", user_id, str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
