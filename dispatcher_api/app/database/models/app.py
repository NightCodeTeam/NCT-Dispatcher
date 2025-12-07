from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey
from ..database import Base
from .incident import Incident


class App(Base):
    __tablename__ = 'apps'

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    code: Mapped[str] = mapped_column(unique=True, nullable=False)
    status_url: Mapped[str] = mapped_column(nullable=True)
    logs_folder: Mapped[str] = mapped_column(nullable=True)

    added_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    added_by: Mapped['User'] = relationship('User', back_populates='apps')

    incidents = relationship(Incident, back_populates='app', cascade='all, delete')
