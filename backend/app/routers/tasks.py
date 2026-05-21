from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas.task import TaskCreate, TaskUpdate, TaskOut, TaskListOut
from ..models.user import User
from ..core.dependencies import get_db, get_current_user
from ..services.task_service import (
    create_task,
    get_tasks,
    get_task_by_id,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskOut, status_code=201)
def create_task_endpoint(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task for the current user."""
    db_task = create_task(
        db, title=task.title, description=task.description, owner_id=current_user.id
    )
    return db_task


@router.get("/", response_model=TaskListOut)
def get_tasks_endpoint(
    page: int = 1,
    page_size: int = 10,
    completed: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all tasks for the current user with pagination and optional filter."""
    tasks, total = get_tasks(db, current_user.id, page, page_size, completed)
    return TaskListOut(tasks=tasks, total=total, page=page, page_size=page_size)


@router.get("/{task_id}", response_model=TaskOut)
def get_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific task by ID."""
    db_task = get_task_by_id(db, task_id, current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=TaskOut)
def update_task_endpoint(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a specific task."""
    db_task = update_task(
        db,
        task_id,
        current_user.id,
        title=task_update.title,
        description=task_update.description,
        completed=task_update.completed,
    )
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}")
def delete_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a specific task."""
    success = delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
