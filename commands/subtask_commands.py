from models.subtask import Subtask
from database import get_db
from datetime import datetime

def create_subtask(title, task_id, user_id):
    db = next(get_db())

    new_subtask = Subtask(
        title=title,
        task_id=task_id,
        user_id=user_id,
        completed=False,
        created_at=datetime.utcnow()
    )

    db.add(new_subtask)
    db.commit()
    db.refresh(new_subtask)

    return {"message": "Subtask created", "subtask_id": new_subtask.id}

def get_subtasks(task_id, user_id):
    db = next(get_db())
    subtasks = db.query(Subtask).filter(Subtask.task_id == task_id, Subtask.user_id == user_id).all()
    return subtasks

def get_subtask_details(subtask_id, user_id):
    db = next(get_db())
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id, Subtask.user_id == user_id).first()
    if not subtask:
        return {"error": "Subtask not found or not authorized"}
    return subtask

def update_subtask(subtask_id, user_id, updates):
    db = next(get_db())
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id, Subtask.user_id == user_id).first()
    if not subtask:
        return {"error": "Subtask not found or not authorized"}

    for key, value in updates.items():
        setattr(subtask, key, value)

    db.commit()
    return {"message": "Subtask updated"}

def delete_subtask(subtask_id, user_id):
    db = next(get_db())
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id, Subtask.user_id == user_id).first()
    if not subtask:
        return {"error": "Subtask not found or not authorized"}

    db.delete(subtask)
    db.commit()
    return {"message": "Subtask deleted"}
