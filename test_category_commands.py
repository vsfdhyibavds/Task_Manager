import pytest
from click.testing import CliRunner
from main import cli
from database import get_db
from models.category import Category
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

def test_category_add_list_delete(runner, db):
    # Create a test user
    user = create_test_user(db)
    user_id = user.id

    # Add a category (interactive input)
    inputs = "\n".join([
        "TestCategory",  # name
        "#FF5733",       # color
        str(user_id)     # user_id
    ]) + "\n"
    result_add = runner.invoke(cli, ['category_add'], input=inputs)
    assert result_add.exit_code == 0
    assert "Category created with ID:" in result_add.output

    # Extract category id from output
    category_id = int(result_add.output.strip().split()[-1])

    # List categories and check if the new category is present
    inputs_list = str(user_id) + "\n"
    result_list = runner.invoke(cli, ['category_list'], input=inputs_list)
    assert result_list.exit_code == 0
    assert "TestCategory" in result_list.output

    # Delete the category (interactive input)
    inputs_delete = "\n".join([
        str(category_id),
        str(user_id)
    ]) + "\n"
    result_delete = runner.invoke(cli, ['category_delete'], input=inputs_delete)
    assert result_delete.exit_code == 0
    assert "Category deleted" in result_delete.output

    # Verify category is deleted by listing again
    result_list_after = runner.invoke(cli, ['category_list'], input=inputs_list)
    assert result_list_after.exit_code == 0
    assert "TestCategory" not in result_list_after.output

def test_update_category(runner, db):
    # Create a test user
    user = create_test_user(db)
    user_id = user.id

    # Add a category to update (interactive input)
    inputs_add = "\n".join([
        "OldCategory",
        "#123456",
        str(user_id)
    ]) + "\n"
    result_add = runner.invoke(cli, ['category_add'], input=inputs_add)
    assert result_add.exit_code == 0
    category_id = int(result_add.output.strip().split()[-1])

    # Update the category (interactive input)
    inputs_update = "\n".join([
        str(category_id),
        str(user_id),
        "NewCategory",
        "#654321"
    ]) + "\n"
    result_update = runner.invoke(cli, ['category_update'], input=inputs_update)
    assert result_update.exit_code == 0
    assert "Category updated" in result_update.output

    # List categories and check if the update is reflected
    inputs_list = str(user_id) + "\n"
    result_list = runner.invoke(cli, ['category_list'], input=inputs_list)
    assert result_list.exit_code == 0
    assert "NewCategory" in result_list.output
    assert "OldCategory" not in result_list.output
