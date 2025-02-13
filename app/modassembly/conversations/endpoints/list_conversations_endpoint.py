from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.modassembly.conversations.business.list_conversations import list_conversations
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.models.repository.Repository import Repository
from app.modassembly.models.conversation.Conversation import Conversation

router = APIRouter()

class ConversationResponse(BaseModel):
    id: int
    repository_id: int
    conversation_type: str
    created_at: str

@router.get(
    "/conversations",
    response_model=List[ConversationResponse],
    summary="List Conversations",
    description=(
        "Retrieve all conversations for a given repository filtered by conversation type "
        "after validating that the repository belongs to the provided user. "
        "Query parameters: repository_id, user_id, and conversation_type."
    )
)
def list_conversations_endpoint(
    repository_id: int,
    user_id: int,
    conversation_type: str = Query(..., description="Type of conversation to filter by"),
    db: Session = Depends(get_sql_session)
) -> List[ConversationResponse]:
    """
    FastAPI endpoint that receives repository_id, user_id, and conversation_type as query
    parameters, validates that the repository belongs to the specified user, and returns all
    conversations of that type related to the repository.

    Parameters:
        repository_id (int): The ID of the repository.
        user_id (int): The ID of the user.
        conversation_type (str): The conversation type to filter by.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        List[ConversationResponse]: A list of conversations filtered by conversation type.
    """
    repository: Repository | None = db.query(Repository).filter(Repository.id == repository_id).first()
    if repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    if repository.user_id != user_id:
        raise HTTPException(status_code=403, detail="Repository does not belong to the specified user")
    
    conversations: List[Conversation] = list_conversations(repository_id)
    filtered_conversations = [
        conv for conv in conversations if conv.conversation_type == conversation_type
    ]
    
    return [
        ConversationResponse(
            id=conv.id,
            repository_id=conv.repository_id,
            conversation_type=conv.conversation_type,
            created_at=conv.created_at.isoformat() if isinstance(conv.created_at, datetime) else str(conv.created_at)
        )
        for conv in filtered_conversations
    ]
