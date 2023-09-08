from sqlalchemy import Column, String, BigInteger, Integer

from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    conversation = Column(String(128), unique=True, nullable=True)
    chat_id = Column(Integer, nullable=True)
