from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.modassembly.database.sql.get_sql_session import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: int = Column(Integer, primary_key=True, index=True)
    repository_id: int = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    type: str = Column(String, nullable=False)
    content: str = Column(String, nullable=False)
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
