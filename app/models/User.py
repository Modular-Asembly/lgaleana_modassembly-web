from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.modassembly.database.sql.get_sql_session import Base


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True, nullable=False)
    email: str = Column(String, unique=True, index=True, nullable=False)
    password_hash: str = Column(String, nullable=False)
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
