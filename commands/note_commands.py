from models.note import Note
from database import get_db
from datetime import datetime

def create_note(content, task_id, user_id):
    db = next(get_db())

    new_note = Note(
        content=content,
        task_id=task_id,
        user_id=user_id,
        created_at=datetime.utcnow()
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {"message": "Note created", "note_id": new_note.id}

def get_notes(task_id, user_id):
    db = next(get_db())
    notes = db.query(Note).filter(Note.task_id == task_id, Note.user_id == user_id).all()
    return notes

def get_note_details(note_id, user_id):
    db = next(get_db())
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        return {"error": "Note not found or not authorized"}
    return note

def update_note(note_id, user_id, updates):
    db = next(get_db())
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        return {"error": "Note not found or not authorized"}

    for key, value in updates.items():
        setattr(note, key, value)

    db.commit()
    return {"message": "Note updated"}

def delete_note(note_id, user_id):
    db = next(get_db())
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        return {"error": "Note not found or not authorized"}

    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}
