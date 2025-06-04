from models.category import Category
from models.task import Task
from database import get_db

def create_category(name, color, user_id):
    db = next(get_db())

    new_category = Category(
        name=name,
        color=color,
        user_id=user_id
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {"message": "Category created", "category_id": new_category.id}

def get_categories(user_id):
    db = next(get_db())
    categories = db.query(Category).filter(Category.user_id == user_id).all()
    return categories

def update_category(category_id, user_id, updates):
    db = next(get_db())

    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id
    ).first()

    if not category:
        return {"error": "Category not found or not authorized"}

    for key, value in updates.items():
        setattr(category, key, value)

    db.commit()
    return {"message": "Category updated"}

def delete_category(category_id, user_id):
    db = next(get_db())

    # Check if category has tasks
    has_tasks = db.query(Task).filter(Task.category_id == category_id).first()
    if has_tasks:
        return {"error": "Cannot delete category with existing tasks"}

    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id
    ).first()

    if not category:
        return {"error": "Category not found or not authorized"}

    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}
