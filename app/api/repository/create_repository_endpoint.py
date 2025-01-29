import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.repository.create_repository import create_repository
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class RepositoryCreateRequest(BaseModel):
    name: str

class RepositoryCreateResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    message: str

@router.post("/repositories", response_model=RepositoryCreateResponse, summary="Create a new repository", tags=["Repositories"])
def create_repository_endpoint(repository_data: RepositoryCreateRequest, user_id: int, db: Session = Depends(get_sql_session)) -> RepositoryCreateResponse:
    """
    Create a new repository.

    - **name**: The name of the repository.
    - **user_id**: The ID of the user who owns the repository.
    """
    logger.info("create_repository_endpoint called with repository_data: %s, user_id: %d", repository_data, user_id)

    try:
        new_repository = create_repository(repository_data.dict(), user_id)
        response = RepositoryCreateResponse(
            id=new_repository.id,
            name=new_repository.name.__str__(),
            owner_id=new_repository.owner_id,
            message="Repository created successfully"
        )
        logger.info("Repository created successfully with id: %d", new_repository.id.__str__())
        return response
    except Exception as e:
        logger.error("Error creating repository: %s", str(e))
        raise HTTPException(status_code=400, detail="Error creating repository")
