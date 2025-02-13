from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.modassembly.database.sql.get_sql_session import Base
from app.modassembly.models.repository.Repository import Repository

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey(Repository.id), nullable=False, index=True)
    conversation_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
