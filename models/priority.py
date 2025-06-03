from sqlalchemy import Column, Integer, String
from database import Base

class Priority(Base):
    __tablename__ = 'priorities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    level = Column(Integer)
    color = Column(String)