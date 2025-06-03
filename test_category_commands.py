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

    # Add a category
    result_add = runner.invoke(cli, ['category_add', '--name', 'TestCategory', '--color', '#FF5733', '--user-id', str(user_id)])
    assert result_add.exit_code == 0
    assert "Category created with ID:" in result_add.output

    # Extract category id from output
    category_id = int(result_add.output.strip().split()[-1])

    # List categories and check if the new category is present
    result_list = runner.invoke(cli, ['category_list', '--user-id', str(user_id)])
    assert result_list.exit_code == 0
    assert "TestCategory" in result_list.output

    # Delete the category
    result_delete = runner.invoke(cli, ['category_delete', '--category-id', str(category_id), '--user-id', str(user_id)])
    assert result_delete.exit_code == 0
    assert "Category deleted" in result_delete.output

    # Verify category is deleted by listing again
    result_list_after = runner.invoke(cli, ['category_list', '--user-id', str(user_id)])
    assert result_list_after.exit_code == 0
    assert "TestCategory" not in result_list_after.output
