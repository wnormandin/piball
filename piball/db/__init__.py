import datetime
from sqlalchemy import create_engine, Column, Integer, DateTime, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Session

from .. import db_url
from .models import ElementModel


db_engine = create_engine(db_url)


class Base(DeclarativeBase):
    pass


class TimestampedRecord(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.now)


class PlayfieldElement(TimestampedRecord):
    __tablename__ = 'elements'

    label = Column(String(25))
    type = Column(String(50))
    location = Column(String(50))
    input = Column(Boolean, default=True)
    output = Column(Boolean, default=False)
    relay_signal = Column(String(5), nullable=True)
    input_label = Column(String(50))
    output_label = Column(String(50))
    input_gpio_pin = Column(Integer)
    output_gpio_pin = Column(Integer, nullable=True)

    @property
    def serialized(self):
        return ElementModel.model_validate(self, from_attributes=True)


def read_db():
    with Session(db_engine) as session:
        return [element.serialized for element in session.query(PlayfieldElement)]
