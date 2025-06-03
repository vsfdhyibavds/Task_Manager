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

def update_user(user_id, updates):
    db = next(get_db())

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    if "username" in updates:
        user.username = updates["username"]
    if "email" in updates:
        user.email = updates["email"]
    if "password" in updates:
        user.password = f"hashed_{updates['password']}"  # Simple hashing

    db.commit()
    return {"message": "User updated successfully"}

def delete_user(user_id):
    db = next(get_db())

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} deleted successfully"}
