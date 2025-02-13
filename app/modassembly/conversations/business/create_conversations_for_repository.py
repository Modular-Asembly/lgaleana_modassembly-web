from typing import Iterator
from sqlalchemy.orm import Session
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.models.conversation.Conversation import Conversation

def create_conversations_for_repository(repository_id: int) -> None:
    session_iter: Iterator[Session] = get_sql_session()
    db: Session = next(session_iter)
    
    # Create two Conversation instances: one for 'brainstorm' and one for 'architecture'
    conversation_brainstorm = Conversation(
        repository_id=repository_id,
        conversation_type="brainstorm"
    )
    conversation_architecture = Conversation(
        repository_id=repository_id,
        conversation_type="architecture"
    )
    
    db.add(conversation_brainstorm)
    db.add(conversation_architecture)
    db.commit()
    
    db.refresh(conversation_brainstorm)
    db.refresh(conversation_architecture)
    
    try:
        next(session_iter)
    except StopIteration:
        pass
