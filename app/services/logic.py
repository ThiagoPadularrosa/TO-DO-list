from app.schemas.userSchema import Todo

def create_new_task(task_data: Todo):
  new_task = {
    "id": 1,
    "title": task_data.title,
    "description": task_data.description,
    "completed": task_data.completed
  }
  return new_task