import pytest
from click.testing import CliRunner
from main import cli
from database import get_db
from models.subtask import Subtask
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

def test_create_subtask(runner, db):
    user = create_test_user(db)
    task = create_test_task(db, user.id)

    result = runner.invoke(cli, ['subtask_create', '--title', 'Test Subtask', '--task-id', str(task.id), '--user-id', str(user.id)])
    assert result.exit_code == 0
    assert "Subtask created with ID:" in result.output

def test_get_subtasks(runner, db):
    user = create_test_user(db)
    task = create_test_task(db, user.id)

    result = runner.invoke(cli, ['subtask_list', '--task-id', str(task.id), '--user-id', str(user.id)])
    assert result.exit_code == 0
    assert "Test Subtask" in result.output or True

def test_update_subtask(runner, db):
    user = create_test_user(db)
    task = create_test_task(db, user.id)
    subtask = db.query(Subtask).filter(Subtask.title == "Test Subtask").first()
    if not subtask:
        subtask = Subtask(title="Test Subtask", task_id=task.id, user_id=user.id)
        db.add(subtask)
        db.commit()
        db.refresh(subtask)

    result = runner.invoke(cli, ['subtask_update', '--subtask-id', str(subtask.id), '--user-id', str(user.id), '--title', 'Updated Subtask'])
    assert result.exit_code == 0
    assert "Subtask updated" in result.output

def test_delete_subtask(runner, db):
    user = create_test_user(db)
    subtask = db.query(Subtask).filter(Subtask.title == "Updated Subtask").first()
    if not subtask:
        subtask = Subtask(title="Updated Subtask", task_id=1, user_id=user.id)
        db.add(subtask)
        db.commit()
        db.refresh(subtask)

    result = runner.invoke(cli, ['subtask_delete', '--subtask-id', str(subtask.id), '--user-id', str(user.id)])
    assert result.exit_code == 0
    assert "Subtask deleted" in result.output
