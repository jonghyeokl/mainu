import datetime

from app.db.base import Base

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    created_dt = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_dt = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
