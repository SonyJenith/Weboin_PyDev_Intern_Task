from sqlalchemy.orm import Session

from ..models.task import Task
from ..models.user import User


def create_task(db: Session, title: str, description: str = None, owner_id: int = None) -> Task:
    """Create a new task."""
    db_task = Task(title=title, description=description, owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, owner_id: int, page: int = 1, page_size: int = 10, completed: bool = None):
    """Retrieve paginated tasks for a user with optional filter."""
    query = db.query(Task).filter(Task.owner_id == owner_id)
    
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    total = query.count()
    tasks = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return tasks, total


def get_task_by_id(db: Session, task_id: int, owner_id: int):
    """Retrieve a task by ID if it belongs to the current user."""
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()


def update_task(db: Session, task_id: int, owner_id: int, title: str = None, description: str = None, completed: bool = None) -> Task:
    """Update a task (partial update)."""
    db_task = get_task_by_id(db, task_id, owner_id)
    if not db_task:
        return None
    
    if title is not None:
        db_task.title = title
    if description is not None:
        db_task.description = description
    if completed is not None:
        db_task.completed = completed
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, owner_id: int) -> bool:
    """Delete a task if it belongs to the current user."""
    db_task = get_task_by_id(db, task_id, owner_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True
