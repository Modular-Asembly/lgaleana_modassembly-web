from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.modassembly.database.sql.get_sql_session import Base
from app.modassembly.models.conversation.Conversation import Conversation

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey(Conversation.id), nullable=False, index=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
