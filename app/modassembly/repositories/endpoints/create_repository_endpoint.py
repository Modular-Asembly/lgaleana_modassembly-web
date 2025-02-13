from fastapi import APIRouter, status
from pydantic import BaseModel
from app.modassembly.repositories.business.create_repository import create_repository
from app.modassembly.models.repository.Repository import Repository

router = APIRouter()

class CreateRepositoryPayload(BaseModel):
    user_id: int
    repo_name: str

class RepositoryResponse(BaseModel):
    id: int
    name: str
    created_at: str
    user_id: int

@router.post(
    "/repositories",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Repository",
    description=(
        "Creates a new repository for the given user. Validates the payload, "
        "ensures the user exists, constructs the repository name, checks that it "
        "does not already exist in the GitHub 'Modular-Asembly' organization, and if "
        "not, creates it via the GitHub API. The repository is then saved in the local "
        "database and details are returned."
    )
)
def create_repository_endpoint(payload: CreateRepositoryPayload) -> RepositoryResponse:
    """
    FastAPI endpoint to create a new repository.

    Parameters:
    - payload: CreateRepositoryPayload
        - user_id: The ID of the user who owns the repository.
        - repo_name: The desired name of the repository.

    Returns:
    - RepositoryResponse containing the repository id, name, created_at timestamp, and user_id.
    """
    repository: Repository = create_repository(payload.user_id, payload.repo_name)
    return RepositoryResponse(
        id=repository.id,
        name=repository.name,
        created_at=repository.created_at.isoformat(),
        user_id=repository.user_id
    )
