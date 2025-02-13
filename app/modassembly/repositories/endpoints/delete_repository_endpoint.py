from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.modassembly.auth.authenticate import authenticate
from app.modassembly.repositories.business.delete_repository import delete_repository

router = APIRouter(
    prefix="/repository",
    tags=["Repository"],
)

class DeleteRepositoryInput(BaseModel):
    repo_name: str

class DeleteRepositoryOutput(BaseModel):
    message: str

@router.delete(
    "",
    response_model=DeleteRepositoryOutput,
    summary="Delete Repository",
    description=(
        "Deletes a repository after authenticating the user using a JWT token. "
        "Requires the repository name in the request payload. The JWT token must be provided "
        "in the 'Authorization' header in the format 'Bearer <token>'."
    ),
)
def delete_repository_endpoint(
    payload: DeleteRepositoryInput,
    authorization: str = Header(..., description="Bearer token")
) -> DeleteRepositoryOutput:
    """
    Endpoint to delete a repository.

    - **repo_name**: The name of the repository (without the username prefix) to be deleted.
    
    The user must supply a valid JWT token in the Authorization header.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    token = authorization[len("Bearer "):].strip()

    user_info = authenticate(token)
    if "id" not in user_info:
        raise HTTPException(status_code=401, detail="Invalid token payload: missing user id")
    user_id = user_info["id"]

    message = delete_repository(user_id=user_id, repo_name=payload.repo_name)
    return DeleteRepositoryOutput(message=message)
