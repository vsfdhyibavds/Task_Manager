from models.task import Task
from models.subtask import Subtask
from models.note import Note
from database import get_db
from datetime import datetime

def create_task(title, description, due_date, priority_id, category_id, user_id):
    db = next(get_db())

    new_task = Task(
        title=title,
        description=description,
        due_date=due_date,
        priority_id=priority_id,
        category_id=category_id,
        user_id=user_id,
        created_at=datetime.utcnow()
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created", "task_id": new_task.id}

def get_tasks(user_id):
    db = next(get_db())
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks

def get_task_details(task_id, user_id):
    db = next(get_db())

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        return {"error": "Task not found or not authorized"}

    subtasks = db.query(Subtask).filter(Subtask.task_id == task_id).all()
    notes = db.query(Note).filter(Note.task_id == task_id).all()

    return {
        "task": task,
        "subtasks": subtasks,
        "notes": notes
    }

def update_task(task_id, user_id, updates):
    db = next(get_db())

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        return {"error": "Task not found or not authorized"}

    for key, value in updates.items():
        setattr(task, key, value)

    db.commit()
    return {"message": "Task updated"}

def delete_task(task_id, user_id):
    db = next(get_db())

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        return {"error": "Task not found or not authorized"}

    # Delete related subtasks and notes first
    db.query(Subtask).filter(Subtask.task_id == task_id).delete()
    db.query(Note).filter(Note.task_id == task_id).delete()

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}