from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class BannedIP(Base):
    __tablename__ = 'bannedips'

    ip: Mapped[str] = mapped_column(primary_key=True)
    reason: Mapped[str]
