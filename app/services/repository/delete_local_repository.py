import logging
from sqlalchemy.orm import Session
from app.models.Repository import Repository
from app.models.Conversation import Conversation
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_local_repository(repository_id: int) -> None:
    """
    Deletes the Repository instance and all associated Conversations from the local database.

    Args:
        repository_id (int): The ID of the repository to delete.
    """
    logger.info("delete_local_repository called with repository_id: %d", repository_id)

    # 1) Accepts repository ID as input
    session: Session = next(get_sql_session())

    try:
        # 2) Deletes the Repository instance from the local database
        repository = session.query(Repository).filter(Repository.id == repository_id).first()
        if repository:
            session.delete(repository)
            logger.info("Deleted repository with id: %d", repository_id)

        # 3) Deletes all associated Conversations
        conversations = session.query(Conversation).filter(Conversation.repository_id == repository_id).all()
        for conversation in conversations:
            session.delete(conversation)
            logger.info("Deleted conversation with id: %d", conversation.id.__str__())

        session.commit()
    finally:
        session.close()
        logger.info("Session closed after deleting repository and conversations.")
