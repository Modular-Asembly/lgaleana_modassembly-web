from datetime import datetime
from typing import List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.modassembly.conversations.business.list_conversations import list_conversations

# Pydantic model for conversation response
class ConversationResponse(BaseModel):
    id: int
    repository_id: int
    conversation_type: str
    created_at: str

router = APIRouter()

@router.get(
    "/conversations",
    response_model=List[ConversationResponse],
    summary="List Conversations",
    description=(
        "Retrieve all conversations related to a given repository by providing the repository ID. "
        "Calls the business function to fetch Conversation records from the database."
    )
)
def list_conversations_endpoint(
    repository_id: int = Query(..., description="ID of the repository to filter conversations")
) -> List[ConversationResponse]:
    """
    FastAPI endpoint that receives a repository ID as a query parameter and returns all conversations 
    related to that repository. The endpoint calls the list_conversations business function and 
    maps each Conversation record into a ConversationResponse model for Swagger documentation.
    
    Parameters:
        repository_id (int): The ID of the repository whose conversations are to be retrieved.
    
    Returns:
        List[ConversationResponse]: A list of conversation responses.
    """
    conversations = list_conversations(repository_id)
    return [
        ConversationResponse(
            id=conv.id,
            repository_id=conv.repository_id,
            conversation_type=conv.conversation_type,
            created_at=conv.created_at.isoformat()
        )
        for conv in conversations
    ]
