from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.modassembly.auth.authenticate import authenticate
from app.modassembly.conversations.business.get_conversation import get_conversation
from app.modassembly.models.conversation.Conversation import Conversation

router: APIRouter = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
    responses={404: {"description": "Not found"}}
)

class ConversationOutput(BaseModel):
    id: int
    repository_id: int
    conversation_type: str
    created_at: datetime

    class Config:
        orm_mode = True

@router.get(
    "/",
    response_model=ConversationOutput,
    summary="Get Conversation",
    description=(
        "Retrieves a conversation belonging to a repository. "
        "You must provide the repository ID, user ID, and conversation type "
        "as query parameters. The endpoint is secured with OAuth2 via JWT token."
    ),
)
def get_conversation_endpoint(
    repository_id: int = Query(..., description="The ID of the repository"),
    user_id: int = Query(..., description="The ID of the owner user"),
    conversation_type: str = Query(..., description="The type of the conversation (e.g., brainstorm, architecture)"),
    token_payload: dict[str, Any] = Depends(authenticate)
) -> ConversationOutput:
    """
    Endpoint to retrieve a conversation for a given repository by conversation type.
    
    Query Parameters:
    - repository_id: The repository's unique identifier.
    - user_id: The user's unique identifier who owns the repository.
    - conversation_type: The type of the conversation to retrieve.
    
    Returns:
        A conversation record matching the query.
    """
    conversation: Conversation = get_conversation(user_id, repository_id, conversation_type)
    return ConversationOutput.from_orm(conversation)
