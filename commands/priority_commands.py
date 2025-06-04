from models.priority import Priority
from database import get_db
from datetime import datetime

def create_priority(name, level, color):
    db = next(get_db())

    new_priority = Priority(
        name=name,
        level=level,
        color=color
    )

    db.add(new_priority)
    db.commit()
    db.refresh(new_priority)

    return {"message": "Priority created", "priority_id": new_priority.id}

def get_priorities():
    db = next(get_db())
    priorities = db.query(Priority).all()
    return priorities

def get_priority_details(priority_id):
    db = next(get_db())
    priority = db.query(Priority).filter(Priority.id == priority_id).first()
    if not priority:
        return {"error": "Priority not found"}
    return priority

def update_priority(priority_id, updates):
    db = next(get_db())
    priority = db.query(Priority).filter(Priority.id == priority_id).first()
    if not priority:
        return {"error": "Priority not found"}

    for key, value in updates.items():
        setattr(priority, key, value)

    db.commit()
    return {"message": "Priority updated"}

def delete_priority(priority_id):
    db = next(get_db())
    priority = db.query(Priority).filter(Priority.id == priority_id).first()
    if not priority:
        return {"error": "Priority not found"}

    db.delete(priority)
    db.commit()
    return {"message": "Priority deleted"}
