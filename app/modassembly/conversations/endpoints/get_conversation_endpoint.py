from datetime import datetime
from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.modassembly.conversations.business.get_conversation import get_conversation
from app.modassembly.models.conversation.Conversation import Conversation

router = APIRouter()

class GetConversationResponse(BaseModel):
    id: int
    repository_id: int
    conversation_type: str
    created_at: datetime

    class Config:
        orm_mode = True

@router.get(
    "/conversation",
    response_model=GetConversationResponse,
    summary="Retrieve a conversation",
    description=(
        "Retrieves a single conversation related to a given repository. "
        "Requires query parameters: repository_id (int), user_id (int), and conversation_type (str). "
        "Validates repository ownership before returning the conversation."
    ),
)
def get_conversation_endpoint(
    repository_id: int = Query(..., description="The repository ID"),
    user_id: int = Query(..., description="The user ID for ownership validation"),
    conversation_type: str = Query(..., description="The type of the conversation")
) -> GetConversationResponse:
    """
    FastAPI endpoint to retrieve a conversation.

    Parameters:
    - repository_id: The ID of the repository.
    - user_id: The ID of the user (for repository ownership validation).
    - conversation_type: The type of conversation to retrieve.

    Returns:
    - GetConversationResponse: The details of the conversation.
    
    Raises:
    - ValueError: If the repository does not belong to the user or no matching conversation is found.
    """
    conversation: Conversation = get_conversation(user_id, repository_id, conversation_type)
    return GetConversationResponse.from_orm(conversation)
