from typing import Iterator

from sqlalchemy.orm import Session

from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.models.conversation.Conversation import Conversation
from app.modassembly.models.repository.Repository import Repository


def get_conversation(user_id: int, repository_id: int, conversation_type: str) -> Conversation:
    session_iter: Iterator[Session] = get_sql_session()
    db: Session = next(session_iter)

    # Validate repository ownership
    repo: Repository | None = (
        db.query(Repository)
        .filter(Repository.id == repository_id, Repository.user_id == user_id)
        .first()
    )
    if repo is None:
        raise ValueError(f"Repository with id {repository_id} not found for user {user_id}")

    conversation: Conversation | None = (
        db.query(Conversation)
        .filter(Conversation.repository_id == repository_id, Conversation.conversation_type == conversation_type)
        .first()
    )
    if conversation is None:
        raise ValueError(
            f"Conversation of type '{conversation_type}' for repository {repository_id} not found"
        )

    try:
        next(session_iter)
    except StopIteration:
        pass

    return conversation
