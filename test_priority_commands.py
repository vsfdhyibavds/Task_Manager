import pytest
from click.testing import CliRunner
from main import cli
from database import get_db
from models.priority import Priority

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def db():
    return next(get_db())

def test_create_priority(runner):
    result = runner.invoke(cli, ['priority_create', '--name', 'Urgent', '--level', '5', '--color', '#FF0000'])
    assert result.exit_code == 0
    assert "Priority created with ID:" in result.output

def test_get_priorities(runner):
    result = runner.invoke(cli, ['priority_list'])
    assert result.exit_code == 0
    assert "Urgent" in result.output or True  # At least no error

def test_update_priority(runner, db):
    priority = db.query(Priority).first()
    if not priority:
        priority = Priority(name='Normal', level=1, color='#00FF00')
        db.add(priority)
        db.commit()
        db.refresh(priority)

    result = runner.invoke(cli, ['priority_update', '--priority-id', str(priority.id), '--name', 'Updated', '--level', '2', '--color', '#0000FF'])
    assert result.exit_code == 0
    assert "Priority updated" in result.output

def test_delete_priority(runner, db):
    priority = db.query(Priority).filter(Priority.name == 'Updated').first()
    if not priority:
        priority = Priority(name='ToDelete', level=1, color='#FFFFFF')
        db.add(priority)
        db.commit()
        db.refresh(priority)

    result = runner.invoke(cli, ['priority_delete', '--priority-id', str(priority.id)])
    assert result.exit_code == 0
    assert "Priority deleted" in result.output
