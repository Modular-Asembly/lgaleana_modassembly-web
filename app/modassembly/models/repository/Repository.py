from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.modassembly.database.sql.get_sql_session import Base
from app.modassembly.models.user.User import User  # Ensure User model is imported for reference

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
