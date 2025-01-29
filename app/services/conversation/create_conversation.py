import logging
from typing import Dict

from sqlalchemy.orm import Session

from app.models.Conversation import Conversation
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_conversation(conversation_data: Dict[str, str], repository_id: int, conversation_type: str) -> Conversation:
    logger.info("create_conversation called with conversation_data: %s, repository_id: %d, conversation_type: %s", conversation_data, repository_id, conversation_type)

    # 1) Accepts conversation data, repository ID, and conversation type as input
    content: str = conversation_data["content"]

    # 2) Creates a new Conversation instance
    new_conversation = Conversation(
        repository_id=repository_id,
        type=conversation_type,
        content=content
    )

    # 3) Saves the Conversation instance to the database
    session: Session = next(get_sql_session())
    session.add(new_conversation)
    session.commit()
    session.refresh(new_conversation)
    session.close()

    logger.info("Conversation created with id: %s", new_conversation.id.__str__())
    return new_conversation
