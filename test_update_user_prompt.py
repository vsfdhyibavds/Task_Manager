import pytest
from click.testing import CliRunner
from update_user_prompt import update_user_prompt

@pytest.fixture
def runner():
    return CliRunner()

def test_no_updates_provided(runner):
    result = runner.invoke(update_user_prompt, input='1\n\n\n\n')
    assert "No updates provided" in result.output

def test_update_username(runner):
    # Assuming user with ID 1 exists
    result = runner.invoke(update_user_prompt, input='1\nnewusername\n\n\n')
    assert "User updated successfully" in result.output or "Error" in result.output

def test_update_email_and_password(runner):
    # Assuming user with ID 1 exists
    result = runner.invoke(update_user_prompt, input='1\n\nnewemail@example.com\nnewpassword\nnewpassword\n')
    assert "User updated successfully" in result.output or "Error" in result.output
