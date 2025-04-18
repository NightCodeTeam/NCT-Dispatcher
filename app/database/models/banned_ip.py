from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer

from ..database import Base


class BannedIP(Base):
    __tablename__ = 'bannedips'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ip: Mapped[str]
    reason: Mapped[str]
