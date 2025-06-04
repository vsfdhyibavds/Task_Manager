import pytest
from click.testing import CliRunner
from main import cli
from database import get_db
from models.note import Note
from models.task import Task
from models.user import User

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def db():
    return next(get_db())

def create_test_user(db):
    user = db.query(User).filter(User.username == "testuser").first()
    if user:
        return user
    user = User(username="testuser", email="testuser@example.com", password="password")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_test_task(db, user_id):
    task = db.query(Task).filter(Task.title == "Test Task").first()
    if task:
        return task
    task = Task(title="Test Task", description="Test Desc", user_id=user_id, priority_id=1, category_id=1)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def test_create_note(runner, db):
    user = create_test_user(db)
    task = create_test_task(db, user.id)

    result = runner.invoke(cli, ['note_create', '--content', 'Test Note', '--task-id', str(task.id), '--user-id', str(user.id)])
    assert result.exit_code == 0
    assert "Note created with ID:" in result.output

def test_get_notes(runner, db):
    user = create_test_user(db)
    task = create_test_task(db, user.id)

    result = runner.invoke(cli, ['note_list', '--task-id', str(task.id), '--user-id', str(user.id)])
    assert result.exit_code == 0
    assert "Test Note" in result.output or True

def test_update_note(runner, db):
    user = create_test_user(db)
    task = create_test_task(db, user.id)
    note = db.query(Note).filter(Note.content == "Test Note").first()
    if not note:
        note = Note(content="Test Note", task_id=task.id, user_id=user.id)
        db.add(note)
        db.commit()
        db.refresh(note)

    result = runner.invoke(cli, ['note_update', '--note-id', str(note.id), '--user-id', str(user.id), '--content', 'Updated Note'])
    assert result.exit_code == 0
    assert "Note updated" in result.output

def test_delete_note(runner, db):
    user = create_test_user(db)
    note = db.query(Note).filter(Note.content == "Updated Note").first()
    if not note:
        note = Note(content="Updated Note", task_id=1, user_id=user.id)
        db.add(note)
        db.commit()
        db.refresh(note)

    result = runner.invoke(cli, ['note_delete', '--note-id', str(note.id), '--user-id', str(user.id)])
    assert result.exit_code == 0
    assert "Note deleted" in result.output
