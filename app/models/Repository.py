from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.modassembly.database.sql.get_sql_session import Base

class Repository(Base):
    __tablename__ = "repositories"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, index=True, nullable=False)
    owner_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
