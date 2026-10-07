from pydantic import BaseModel
from typing import Optional

# The data structure (Schema) across reading and creation to validate the user send a correct str or int
class TaskBase(BaseModel):
  title: str
  description: Optional[str] = None

# Schema for the incoming request data when creating a task
class TaskCreate(TaskBase):
  pass

class TaskResponse(TaskBase):
  id: int
  is_completed: bool

  class Config:
      from_attributes = True # This allow Pydantic to read SQLAlchemy models

class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False