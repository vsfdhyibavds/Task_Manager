import click
from commands.user_commands import register_user, login_user, update_user
from commands.task_commands import (
    create_task, get_tasks, get_task_details,
    update_task, delete_task
)
from commands.category_commands import (
    create_category, get_categories, delete_category
)
from init_db import init_db
from datetime import datetime

@click.group()
def cli():
    """Task Manager CLI"""
    pass

@cli.command()
def init():
    """Initialize the database"""
    init_db()
    click.echo("Database initialized")

@cli.command()
@click.option('--username', prompt=True)
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def register(username, email, password):
    """Register a new user"""
    result = register_user(username, email, password)
    if 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(f"User created with ID: {result['user_id']}")

@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(username, password):
    """Login a user"""
    result = login_user(username, password)
    if 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(f"Login successful. Token: {result['token']}")

@cli.command()
@click.option('--user-id', prompt=True, type=int)
@click.option('--username', required=False)
@click.option('--email', required=False)
@click.option('--password', required=False, hide_input=True)
def update_user(user_id, username, email, password):
    """Update user details"""
    updates = {}
    if username:
        updates['username'] = username
    if email:
        updates['email'] = email
    if password:
        updates['password'] = password

    if not updates:
        click.echo("No updates provided")
        return

    from commands.user_commands import update_user as update_user_func
    result = update_user_func(user_id, updates)
    if 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(result['message'])

@cli.command()
@click.option('--title', prompt=True)
@click.option('--description', prompt=True)
@click.option('--due-date', prompt=True, type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option('--priority-id', prompt=True, type=int)
@click.option('--category-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def add(title, description, due_date, priority_id, category_id, user_id):
    """Add a new task"""
    result = create_task(
        title=title,
        description=description,
        due_date=due_date,
        priority_id=priority_id,
        category_id=category_id,
        user_id=user_id
    )
    click.echo(f"Task created with ID: {result['task_id']}")

@cli.command()
@click.option('--user-id', prompt=True, type=int)
def list(user_id):
    """List all tasks"""
    tasks = get_tasks(user_id)
    for task in tasks:
        click.echo(f"{task.id}: {task.title} (Due: {task.due_date})")

@cli.command()
@click.option('--task-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def show(task_id, user_id):
    """Show task details"""
    result = get_task_details(task_id, user_id)
    if 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        task = result['task']
        click.echo(f"Title: {task.title}")
        click.echo(f"Description: {task.description}")
        click.echo(f"Due: {task.due_date}")
        click.echo("\nSubtasks:")
        for subtask in result['subtasks']:
            click.echo(f" - {subtask.title} ({'✓' if subtask.completed else ' '})")
        click.echo("\nNotes:")
        for note in result['notes']:
            click.echo(f" - {note.content}")

@cli.command()
@click.option('--task-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def delete(task_id, user_id):
    """Delete a task"""
    result = delete_task(task_id, user_id)
    click.echo(result['message'])

@cli.command()
@click.option('--name', prompt=True)
@click.option('--color', prompt=True)
@click.option('--user-id', prompt=True, type=int)
def category_add(name, color, user_id):
    """Add a new category"""
    result = create_category(name, color, user_id)
    click.echo(f"Category created with ID: {result['category_id']}")

@cli.command()
@click.option('--user-id', prompt=True, type=int)
def category_list(user_id):
    """List all categories"""
    categories = get_categories(user_id)
    for category in categories:
        click.echo(f"{category.id}: {category.name} ({category.color})")

@cli.command()
@click.option('--category-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def category_delete(category_id, user_id):
    """Delete a category"""
    result = delete_category(category_id, user_id)
    if 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(result['message'])

if __name__ == '__main__':
    cli()
