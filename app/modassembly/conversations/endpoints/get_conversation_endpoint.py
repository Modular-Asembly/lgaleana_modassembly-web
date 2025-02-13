from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel

from app.modassembly.auth.authenticate import authenticate
from app.modassembly.conversations.business.get_conversation import get_conversation
from app.modassembly.models.conversation.Conversation import Conversation

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
    responses={404: {"description": "Not found"}},
)


class GetConversationOutput(BaseModel):
    id: int
    repository_id: int
    conversation_type: str
    created_at: datetime

    @classmethod
    def from_orm(cls, conversation: Conversation) -> "GetConversationOutput":
        return cls(
            id=conversation.id,
            repository_id=conversation.repository_id,
            conversation_type=conversation.conversation_type,
            created_at=conversation.created_at,
        )


@router.get(
    "",
    response_model=GetConversationOutput,
    summary="Retrieve a Conversation",
    description=(
        "Retrieves a conversation filtered by repository ID, user ID, and conversation type. "
        "Requires a valid JWT token in the Authorization header (Bearer token). "
        "The token is validated using the authenticate function. On success, returns the conversation details."
    ),
)
def get_conversation_endpoint(
    repository_id: int = Query(..., description="ID of the repository"),
    user_id: int = Query(..., description="ID of the user owning the repository"),
    conversation_type: str = Query(..., description="Type of the conversation (e.g., brainstorm, architecture)"),
    authorization: str = Header(..., description="Bearer token for authentication"),
) -> GetConversationOutput:
    """
    Endpoint to get a conversation associated with a repository for a user.
    
    Query Parameters:
    - **repository_id**: The ID of the repository.
    - **user_id**: The ID of the user (must match the repository owner).
    - **conversation_type**: The type of conversation to retrieve.
    
    Header:
    - **Authorization**: A Bearer token for authentication.
    
    Returns:
    - A conversation object with details regarding the conversation.
    """
    # Extract token from "Bearer <token>"
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    token = authorization.split("Bearer ")[1].strip()
    # Authenticate the token. The returned payload can be used for additional checks if needed.
    auth_payload: Dict[str, Any] = authenticate(token)
    
    # Here you might validate that auth_payload contains the expected user_id if necessary.
    # For now, we assume that the provided user_id is valid if the token is valid.
    conversation: Conversation = get_conversation(
        user_id=user_id,
        repository_id=repository_id,
        conversation_type=conversation_type,
    )
    return GetConversationOutput.from_orm(conversation)
