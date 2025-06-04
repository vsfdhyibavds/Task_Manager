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
@click.option('--title', prompt=True, required=False)
@click.option('--description', prompt=True, required=False)
@click.option('--due-date', prompt=True, required=False, type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option('--priority-id', prompt=True, required=False, type=int)
@click.option('--category-id', prompt=True, required=False, type=int)
def update(task_id, user_id, title, description, due_date, priority_id, category_id):
    """Update a task"""
    updates = {}
    if title:
        updates['title'] = title
    if description:
        updates['description'] = description
    if due_date:
        updates['due_date'] = due_date
    if priority_id:
        updates['priority_id'] = priority_id
    if category_id:
        updates['category_id'] = category_id

    if not updates:
        click.echo("No updates provided")
        return

    result = update_task(task_id, user_id, updates)
    if 'message' in result:
        click.echo(result['message'])
    elif 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo("Unknown response from update_task")

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

@cli.command()
@click.option('--task-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def delete(task_id, user_id):
    """Delete a task"""
    result = delete_task(task_id, user_id)
    if 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(result['message'])

from commands.note_commands import (
    create_note, get_notes, get_note_details,
    update_note, delete_note
)
from commands.subtask_commands import (
    create_subtask, get_subtasks, get_subtask_details,
    update_subtask, delete_subtask
)

@cli.command()
@click.option('--content', prompt=True)
@click.option('--task-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def note_add(content, task_id, user_id):
    """Add a new note"""
    result = create_note(content, task_id, user_id)
    click.echo(f"Note created with ID: {result['note_id']}")

@cli.command()
@click.option('--task-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def note_list(task_id, user_id):
    """List all notes for a task"""
    notes = get_notes(task_id, user_id)
    for note in notes:
        click.echo(f"{note.id}: {note.content}")

@cli.command()
@click.option('--note-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def note_show(note_id, user_id):
    """Show note details"""
    result = get_note_details(note_id, user_id)
    if isinstance(result, dict) and 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(f"Content: {result.content}")

@cli.command()
@click.option('--note-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
@click.option('--content', prompt=True, required=False)
def note_update(note_id, user_id, content):
    """Update a note"""
    updates = {}
    if content:
        updates['content'] = content

    if not updates:
        click.echo("No updates provided")
        return

    result = update_note(note_id, user_id, updates)
    if 'message' in result:
        click.echo(result['message'])
    elif 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo("Unknown response from update_note")

@cli.command()
@click.option('--note-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def note_delete(note_id, user_id):
    """Delete a note"""
    result = delete_note(note_id, user_id)
    if 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(result['message'])

@cli.command()
@click.option('--title', prompt=True)
@click.option('--task-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def subtask_add(title, task_id, user_id):
    """Add a new subtask"""
    result = create_subtask(title, task_id, user_id)
    click.echo(f"Subtask created with ID: {result['subtask_id']}")

@cli.command()
@click.option('--task-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def subtask_list(task_id, user_id):
    """List all subtasks for a task"""
    subtasks = get_subtasks(task_id, user_id)
    for subtask in subtasks:
        click.echo(f"{subtask.id}: {subtask.title} ({'✓' if subtask.completed else ' '})")

@cli.command()
@click.option('--subtask-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def subtask_show(subtask_id, user_id):
    """Show subtask details"""
    result = get_subtask_details(subtask_id, user_id)
    if isinstance(result, dict) and 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(f"Title: {result.title}")
        click.echo(f"Completed: {'Yes' if result.completed else 'No'}")

@cli.command()
@click.option('--subtask-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
@click.option('--title', prompt=True, required=False)
@click.option('--completed', prompt=True, required=False, type=bool)
def subtask_update(subtask_id, user_id, title, completed):
    """Update a subtask"""
    updates = {}
    if title:
        updates['title'] = title
    if completed is not None:
        updates['completed'] = completed

    if not updates:
        click.echo("No updates provided")
        return

    result = update_subtask(subtask_id, user_id, updates)
    if 'message' in result:
        click.echo(result['message'])
    elif 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo("Unknown response from update_subtask")

@cli.command()
@click.option('--subtask-id', prompt=True, type=int)
@click.option('--user-id', prompt=True, type=int)
def subtask_delete(subtask_id, user_id):
    """Delete a subtask"""
    result = delete_subtask(subtask_id, user_id)
    if 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(result['message'])

from commands.priority_commands import delete_priority

@cli.command()
@click.option('--priority-id', prompt=True, type=int)
def priority_delete(priority_id):
    """Delete a priority"""
    result = delete_priority(priority_id)
    if 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(result['message'])

from commands.priority_commands import delete_priority

@cli.command()
@click.option('--priority-id', prompt=True, type=int)
def priority_delete(priority_id):
    """Delete a priority"""
    result = delete_priority(priority_id)
    if 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(result['message'])

if __name__ == '__main__':
    cli()
