from __future__ import annotations
from typing import List
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base
from .incident import Incident


class App(Base):
    __tablename__ = 'apps'

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    url: Mapped[str]
    dispatcher_code: Mapped[str]
    incidents = relationship(Incident, back_populates='app')
