import logging
from typing import List
from sqlalchemy.orm import Session
from app.models.Repository import Repository
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_repositories(user_id: int) -> List[Repository]:
    """
    Retrieves all repositories associated with the given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Repository]: A list of Repository instances.
    """
    logger.info("get_user_repositories called with user_id: %d", user_id)

    session: Session = next(get_sql_session())
    try:
        # 2) Queries the database for all repositories associated with the given user ID
        repositories = session.query(Repository).filter(Repository.owner_id == user_id).all()
        logger.info("Retrieved %d repositories for user_id: %d", len(repositories), user_id)

        # 3) Returns a list of repositories
        return repositories
    finally:
        session.close()
        logger.info("Session closed after retrieving repositories.")
