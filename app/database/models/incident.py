from datetime import datetime
from typing import Literal

from core.debug.debug_dataclass import Level
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from ..database import Base


class Incident(Base):
    __tablename__ = 'incidents'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    message: Mapped[str]
    logs: Mapped[str]
    level: Mapped[Level]

    status: Mapped[Literal['open', 'closed']] = mapped_column(default='open')

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    app_id: Mapped[int] = mapped_column(ForeignKey('apps.id'))
    app = relationship('App', back_populates='incidents')