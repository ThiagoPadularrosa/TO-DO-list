from fastapi import APIRouter, HTTPException
from app.schemas.userSchema import Todo
from app.services.logic import create_new_task

router = APIRouter(prefix="/user", tags=["tasks"])
  
@router.post("/task/add")
async def add_task(task: Todo):
  try:
    result = create_new_task(task)
    return {"status": "success", "message": "Task added and created successfully", "data": result}
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

@router.get("/task/view")
async def view_task(task_id: int, name: Todo):
  return {"task_id": task_id, "name": name}

@router.put("/task/change")
async def change_task():
  return {}

@router.delete("/task/delete")
async def delete_task():
  return {}