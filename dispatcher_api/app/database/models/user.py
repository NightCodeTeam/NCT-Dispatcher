from typing import List
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]
    last_active: Mapped[datetime] = mapped_column(default=func.now())

    apps: Mapped[List['App']] = relationship('App', back_populates='added_by')
    edited_incidents: Mapped[List['Incident']] = relationship('Incident', back_populates='edit_by')

    def __str__(self):
        return f'User - {self.name}'

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, password={self.password} \
        last_active={self.last_active})'
