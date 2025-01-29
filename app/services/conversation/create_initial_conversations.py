import logging
from sqlalchemy.orm import Session
from app.models.Conversation import Conversation
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_initial_conversations(repository_id: int) -> None:
    """
    Creates two conversations named 'brainstorm' and 'architecture' for the given repository ID.

    Args:
        repository_id (int): The ID of the repository.
    """
    logger.info("create_initial_conversations called with repository_id: %d", repository_id)

    # 2) Creates two conversations named 'brainstorm' and 'architecture'
    conversation_types = ["brainstorm", "architecture"]

    session: Session = next(get_sql_session())
    try:
        for conversation_type in conversation_types:
            new_conversation = Conversation(
                repository_id=repository_id,
                type=conversation_type
            )
            session.add(new_conversation)
            session.commit()
            session.refresh(new_conversation)
            logger.info("Created conversation with id: %d, type: %s", new_conversation.id, new_conversation.type.__str__())
    finally:
        session.close()
