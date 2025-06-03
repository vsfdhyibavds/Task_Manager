from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from datetime import datetime

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    created_at = Column(DateTime, default=datetime.utcnow)