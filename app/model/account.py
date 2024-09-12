from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import UUIDType

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    name = Column(String)
