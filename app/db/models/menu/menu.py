import datetime
import uuid

from app.db.base import Base

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID


class Menu(Base):
    __tablename__ = "menus"

    menu_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    created_dt = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_dt = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
