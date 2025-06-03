import pytest
from click.testing import CliRunner
from main import cli
from unittest.mock import patch
import datetime

@pytest.fixture
def runner():
    return CliRunner()

@patch('main.create_task')
def test_add_task_command(mock_create_task, runner):
    mock_create_task.return_value = {"message": "Task created", "task_id": 1}

    inputs = "\n".join([
        "Test Task",          # title
        "Test Description",   # description
        "2024-12-31",         # due_date
        "1",                  # priority_id
        "1",                  # category_id
        "1"                   # user_id
    ])

    result = runner.invoke(cli, ['add'], input=inputs)

    assert result.exit_code == 0
    assert "Task created with ID: 1" in result.output
    mock_create_task.assert_called_once_with(
        title="Test Task",
        description="Test Description",
        due_date=pytest.approx(datetime.datetime(2024, 12, 31), rel=1),
        priority_id=1,
        category_id=1,
        user_id=1
    )

@patch('main.delete_task')
def test_delete_task_command(mock_delete_task, runner):
    mock_delete_task.return_value = {"message": "Task deleted"}

    inputs = "1\n1\n"

    result = runner.invoke(cli, ['delete'], input=inputs)

    assert result.exit_code == 0
    assert "Task deleted" in result.output
    mock_delete_task.assert_called_once_with(1, 1)

@patch('main.update_task')
def test_update_task_command(mock_update_task, runner):
    mock_update_task.return_value = {"message": "Task updated"}

    inputs = "\n".join([
        "1",
        "1",
        "Updated Title",
        "Updated Description",
        "2024-12-31",
        "2",
        "3"
    ]) + "\n"

    result = runner.invoke(cli, ['update'], input=inputs)

    assert result.exit_code == 0
    assert "Task updated" in result.output
    mock_update_task.assert_called_once_with(1, 1, {
        "title": "Updated Title",
        "description": "Updated Description",
        "due_date": mock_update_task.call_args[0][2]["due_date"],  # datetime object
        "priority_id": 2,
        "category_id": 3
    })
