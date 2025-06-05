Generic single-database configuration.

# Task Manager CLI Application

## Description
This is a Command Line Interface (CLI) based Task Manager application built with Python. It allows users to register, login, and manage tasks, categories, notes, and subtasks efficiently. The project uses Click for CLI commands, SQLAlchemy for ORM and database interactions, and Alembic for database migrations.

## Features
- User registration, login, and update
- Task creation, listing, detail viewing, updating, and deletion
- Category creation, listing, and deletion
- Notes creation, listing, detail viewing, updating, and deletion
- Subtasks creation, listing, detail viewing, updating, and deletion
- Database initialization with dummy data including users, priorities, categories, tasks, subtasks, and notes

## Installation

### Prerequisites
- Python 3.8 or higher

### Install dependencies
```bash
pip install -r requirements.txt
```

## Database Initialization

Initialize the database and populate it with dummy data by running the following CLI command:

```bash
python main.py init
```

Alternatively, you can run the initialization script directly:

```bash
python init_db.py or python3 init_db.py
```

## Usage

The CLI provides the following commands:

- `init` - Initialize the database
- `register` - Register a new user (prompts for username, email, password)
- `login` - Login a user (prompts for username, password)
- `update-user` - Update user details (prompts for user ID and optional fields)
- `add` - Add a new task (prompts for title, description, due date, priority ID, category ID, user ID)
- `list` - List all tasks for a user (prompts for user ID)
- `show` - Show task details including subtasks and notes (prompts for task ID and user ID)
- `delete` - Delete a task (prompts for task ID and user ID)
- `category-add` - Add a new category (prompts for name, color, user ID)
- `category-list` - List all categories for a user (prompts for user ID)
- `category-delete` - Delete a category (prompts for category ID and user ID)
- `note-add` - Add a new note (prompts for content, task ID, user ID)
- `note-list` - List all notes for a task (prompts for task ID, user ID)
- `note-show` - Show note details (prompts for note ID, user ID)
- `note-update` - Update a note (prompts for note ID, user ID, content)
- `note-delete` - Delete a note (prompts for note ID, user ID)
- `subtask-add` - Add a new subtask (prompts for title, task ID, user ID)
- `subtask-list` - List all subtasks for a task (prompts for task ID, user ID)
- `subtask-show` - Show subtask details (prompts for subtask ID, user ID)
- `subtask-update` - Update a subtask (prompts for subtask ID, user ID, title, completed)
- `subtask-delete` - Delete a subtask (prompts for subtask ID, user ID)

Example usage:

```bash
python main.py register
python main.py login
python main.py add
python main.py update
python main.py list
python main.py delete
python main.py category-add
python main.py category-list
python main.py category-delete
python main.py note-add
python main.py subtask-add
```

## Testing

There is a test file `test_register_duplicate_email.py` to check for duplicate email registration scenarios.

Tests for task commands (add, update, delete) are implemented and passing.

Tests for notes and subtasks commands are to be added.

Additional tests have been implemented for full CRUD operations on categories, users, priorities, subtasks, and notes to ensure complete coverage and functionality.

## Notes

- Passwords are hashed in a simple manner for demonstration purposes. For production, use proper password hashing.
- The login command returns a dummy token.
- The database is initialized with sample data for priorities, users, categories, tasks, subtasks, and notes.

## License

This project is provided as-is without any explicit license.
