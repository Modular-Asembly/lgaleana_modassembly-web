import logging
from typing import Dict

from sqlalchemy.orm import Session

from app.models.Repository import Repository
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_repository(repository_data: Dict[str, str], user_id: int) -> Repository:
    logger.info("create_repository called with repository_data: %s, user_id: %d", repository_data, user_id)

    # 1) Accepts repository data and user ID as input
    name: str = repository_data["name"]

    # 2) Creates a new Repository instance
    new_repository = Repository(
        name=name,
        owner_id=user_id
    )

    # 3) Saves the Repository instance to the database
    session: Session = next(get_sql_session())
    session.add(new_repository)
    session.commit()
    session.refresh(new_repository)
    session.close()

    logger.info("Repository created with id: %d", new_repository.id.__str__())
    return new_repository
