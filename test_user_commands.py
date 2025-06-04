import pytest
from click.testing import CliRunner
from main import cli
from database import get_db
from models.user import User

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def db():
    return next(get_db())

def test_register_user(runner, db):
    # Register a new user
    result = runner.invoke(cli, ['register_user', '--username', 'testuser', '--email', 'testuser@example.com', '--password', 'password'])
    assert result.exit_code == 0
    assert "User testuser created successfully" in result.output

def test_login_user(runner, db):
    # Ensure user exists
    user = db.query(User).filter(User.username == 'testuser').first()
    if not user:
        user = User(username='testuser', email='testuser@example.com', password='hashed_password')
        db.add(user)
        db.commit()
        db.refresh(user)

    # Login user
    result = runner.invoke(cli, ['login_user', '--username', 'testuser', '--password', 'password'])
    assert result.exit_code == 0
    assert "Login successful" in result.output

def test_update_user(runner, db):
    # Ensure user exists
    user = db.query(User).filter(User.username == 'testuser').first()
    if not user:
        user = User(username='testuser', email='testuser@example.com', password='hashed_password')
        db.add(user)
        db.commit()
        db.refresh(user)

    # Update user
    result = runner.invoke(cli, ['update_user', '--user-id', str(user.id), '--username', 'updateduser', '--email', 'updated@example.com', '--password', 'newpassword'])
    assert result.exit_code == 0
    assert "User updated successfully" in result.output

def test_delete_user(runner, db):
    # Ensure user exists
    user = db.query(User).filter(User.username == 'updateduser').first()
    if not user:
        user = User(username='updateduser', email='updated@example.com', password='hashed_password')
        db.add(user)
        db.commit()
        db.refresh(user)

    # Delete user
    result = runner.invoke(cli, ['delete_user', '--user-id', str(user.id)])
    assert result.exit_code == 0
    assert f"User with ID {user.id} deleted successfully" in result.output
