from typing import List, Iterator
from sqlalchemy.orm import Session
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.models.conversation.Conversation import Conversation

def list_conversations(repository_id: int) -> List[Conversation]:
    session_iter: Iterator[Session] = get_sql_session()
    db: Session = next(session_iter)
    conversations: List[Conversation] = db.query(Conversation).filter(
        Conversation.repository_id == repository_id
    ).all()
    try:
        next(session_iter)
    except StopIteration:
        pass
    return conversations
