from models.user import User
from database import get_db
from datetime import datetime

def register_user(username, email, password):
    db = next(get_db())

    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return {"error": "Username or email already exists"}

    new_user = User(
        username=username,
        email=email,
        password=f"hashed_{password}",  # In real app, use proper hashing
        created_at=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"User {username} created successfully", "user_id": new_user.id}

def login_user(username, password):
    db = next(get_db())

    user = db.query(User).filter(User.username == username).first()
    if not user or not user.password.endswith(password):  # Simple check for demo
        return {"error": "Invalid credentials"}

    return {
        "message": "Login successful",
        "token": f"dummy_token_{user.id}_{datetime.utcnow().timestamp()}"
    }