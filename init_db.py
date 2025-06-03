# init_db.py
from database import engine, Base
from models.user import User
from models.priority import Priority
from models.category import Category
from models.task import Task
from models.subtask import Subtask
from models.note import Note
from sqlalchemy.orm import sessionmaker
from datetime import datetime

def init_db():
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if data already exists
    if session.query(User).count() > 0:
        print("Database already initialized")
        return

    # Create priorities
    priorities = [
        Priority(name="Low", level=1, color="#4CAF50"),
        Priority(name="Medium", level=2, color="#FFC107"),
        Priority(name="High", level=3, color="#F44336"),
        Priority(name="Critical", level=4, color="#9C27B0")
    ]
    session.add_all(priorities)

    # Create users
    users = [
        User(
            username="john_doe",
            email="john.doe@example.com",
            password="hashed_password_123",
            created_at=datetime(2023, 5, 15, 10, 30)
        ),
        User(
            username="jane_smith",
            email="jane.smith@example.com",
            password="hashed_password_456",
            created_at=datetime(2023, 6, 20, 14, 15)
        ),
        User(
            username="mike_johnson",
            email="mike.j@example.com",
            password="hashed_password_789",
            created_at=datetime(2023, 7, 10, 9, 45)
        )
    ]
    session.add_all(users)
    session.commit()

    # Create categories
    categories = [
        Category(name="Work", color="#4287f5", user_id=1),
        Category(name="Personal", color="#41f5a8", user_id=1),
        Category(name="Study", color="#f541b0", user_id=2),
        Category(name="Health", color="#f5a741", user_id=3)
    ]
    session.add_all(categories)
    session.commit()

    # Create tasks
    tasks = [
        Task(
            title="Complete project proposal",
            description="Finish the 10-page proposal for the client project",
            due_date=datetime(2023, 11, 15, 18, 0),
            completed=False,
            priority_id=2,
            category_id=1,
            user_id=1,
            created_at=datetime(2023, 10, 1, 9, 0)
        ),
        Task(
            title="Grocery shopping",
            description="Buy milk, eggs, bread, and vegetables",
            due_date=datetime(2023, 10, 10, 12, 0),
            completed=True,
            priority_id=1,
            category_id=2,
            user_id=1,
            created_at=datetime(2023, 10, 5, 17, 30)
        ),
        # Add more tasks as needed
    ]
    session.add_all(tasks)
    session.commit()

    # Create subtasks
    subtasks = [
        Subtask(
            title="Research competitors",
            description="Find 3 competing products",
            completed=True,
            task_id=1,
            created_at=datetime(2023, 10, 1, 9, 15)
        ),
        # Add more subtasks as needed
    ]
    session.add_all(subtasks)
    session.commit()

    # Create notes
    notes = [
        Note(
            content="Client mentioned they prefer bullet points over long paragraphs",
            task_id=1,
            created_at=datetime(2023, 10, 3, 15, 30)
        ),
        # Add more notes as needed
    ]
    session.add_all(notes)
    session.commit()

    print("Database initialized with dummy data")

if __name__ == "__main__":
    init_db()