from typing import Iterator
from sqlalchemy.orm import Session

from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.models.conversation.Conversation import Conversation

def delete_conversations_for_repository(repository_id: int) -> None:
    session_iter: Iterator[Session] = get_sql_session()
    db: Session = next(session_iter)
    
    db.query(Conversation).filter(Conversation.repository_id == repository_id).delete(synchronize_session=False)
    db.commit()
    
    try:
        next(session_iter)
    except StopIteration:
        pass
