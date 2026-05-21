from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        from_attributes = True


class TaskListOut(BaseModel):
    tasks: List[TaskOut]
    total: int
    page: int
    page_size: int
