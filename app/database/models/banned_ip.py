from ..database import Base
from sqlalchemy import Column, Integer, String


class BannedIP(Base):
    __tablename__ = 'bannedips'

    ip = Column(String, primary_key=True)
    reason = Column(String(100), nullable=False, default='')
