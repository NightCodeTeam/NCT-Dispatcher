from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from ..database import Base


class BannedIP(Base):
    __tablename__ = 'bannedips'
    ip: Mapped[str] = mapped_column(String, primary_key=True)
    reason: Mapped[str]
