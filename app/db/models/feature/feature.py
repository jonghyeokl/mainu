import datetime

from app.db.base import Base

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY


class Feature(Base):
    __tablename__ = "features"

    feature_id = Column(Integer, primary_key=True, autoincrement=True)
    feature = Column(String, nullable=False)
    available_values = Column(ARRAY(String), nullable=False)

    created_dt = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_dt = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
