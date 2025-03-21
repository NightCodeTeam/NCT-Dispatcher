from __future__ import annotations
from typing import List
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer
from ..database import Base


class Incident(Base):
    __tablename__ = 'incidents'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    message: Mapped[str]
    logs: Mapped[str]
    level: Mapped[str]

    app_id: Mapped[int] = mapped_column(ForeignKey('apps.id'))
    app = relationship('App', back_populates='incidents')