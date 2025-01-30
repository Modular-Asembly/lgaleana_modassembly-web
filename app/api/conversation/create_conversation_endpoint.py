import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.auth.authenticate_request import authenticate_request
from app.services.conversation.create_conversation import create_conversation
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.models.User import User
from app.models.Conversation import Conversation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class ConversationRequest(BaseModel):
    content: str
    repository_id: int
    conversation_type: str

class ConversationResponse(BaseModel):
    message: str
    conversation_id: int

@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation_endpoint(
    conversation_request: ConversationRequest,
    db: Session = Depends(get_sql_session),
    current_user: User = Depends(authenticate_request)
) -> ConversationResponse:
    """
    Endpoint to create a new conversation.

    - **content**: The content of the conversation.
    - **repository_id**: The ID of the repository associated with the conversation.
    - **conversation_type**: The type of the conversation.

    Returns a success message and the conversation ID if creation is successful, otherwise returns an error message.
    """
    logger.info("create_conversation_endpoint called with repository_id: %d, conversation_type: %s",
                conversation_request.repository_id, conversation_request.conversation_type)

    try:
        conversation: Conversation = create_conversation(
            conversation_data={"content": conversation_request.content},
            repository_id=conversation_request.repository_id,
            conversation_type=conversation_request.conversation_type
        )

        response = ConversationResponse(
            message="Conversation created successfully",
            conversation_id=conversation.id
        )

        logger.info("Conversation created with id: %d", conversation.id)
        return response

    except Exception as e:
        logger.error("Error creating conversation: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating conversation"
        )
