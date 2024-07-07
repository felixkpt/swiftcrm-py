from sqlalchemy import Column, Integer, String, DateTime, func
from app.models.base import Base

class TokenBlacklist(Base):
    __tablename__ = 'token_blacklist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(500), nullable=False)
    blacklisted_at = Column(DateTime, nullable=False, server_default=func.now())
