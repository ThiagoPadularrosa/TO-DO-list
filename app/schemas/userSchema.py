from pydantic import BaseModel

# The data structure (Schema)
class Todo(BaseModel):
  title: str
  description: str = ""
  completed: bool = False