from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from database import Base
from datetime import datetime

class Subtask(Base):
    __tablename__ = 'subtasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    created_at = Column(DateTime, default=datetime.utcnow)