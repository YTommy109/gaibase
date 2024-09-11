from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from sqlalchemy import Column, String

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    name = Column(String)
