from sqlalchemy import Column, Integer, String
from app.modassembly.database.sql.get_sql_session import Base


class ConversationType(Base):
    __tablename__ = "conversation_types"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, index=True, nullable=False)
    description: str = Column(String, nullable=True)
