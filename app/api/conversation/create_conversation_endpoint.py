import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.conversation.create_conversation import create_conversation
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class ConversationCreateRequest(BaseModel):
    content: str
    repository_id: int
    conversation_type: str

class ConversationCreateResponse(BaseModel):
    id: int
    message: str

@router.post("/conversations", response_model=ConversationCreateResponse, summary="Create a new conversation", tags=["Conversations"])
def create_conversation_endpoint(conversation_data: ConversationCreateRequest, db: Session = Depends(get_sql_session)) -> ConversationCreateResponse:
    """
    Create a new conversation.

    - **content**: The content of the conversation.
    - **repository_id**: The ID of the repository associated with the conversation.
    - **conversation_type**: The type of the conversation as a string.
    """
    logger.info("create_conversation_endpoint called with conversation_data: %s", conversation_data)

    try:
        new_conversation = create_conversation(conversation_data.dict(), conversation_data.repository_id, conversation_data.conversation_type)
        response = ConversationCreateResponse(
            id=new_conversation.id,
            message="Conversation created successfully"
        )
        logger.info("Conversation created successfully with id: %s", new_conversation.id.__str__())
        return response
    except Exception as e:
        logger.error("Error creating conversation: %s", str(e))
        raise HTTPException(status_code=400, detail="Error creating conversation")
