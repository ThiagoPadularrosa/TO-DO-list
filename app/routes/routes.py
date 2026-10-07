from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database.dbConnection import get_db
from app.schemas.schema import TaskResponse, TaskCreate, TaskUpdate
from app.database.crud import create_task, get_task_by_id, get_all_tasks, update_task, delete_task

router = APIRouter(prefix="/user", tags=["tasks"])

@router.post("/task/add", response_model=TaskResponse, status_code=201)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
  return create_task(db=db, task=task)

@router.get("/task/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
  db_task = get_task_by_id(db, task_id=task_id)
  if db_task is None:
    raise HTTPException(status_code=404, detail="Task not found")
  return db_task

@router.get("/task/", response_model=list[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  tasks = get_all_tasks(db, skip=skip, limit=limit)
  return tasks
  
@router.put("/task/{task_id}", response_model=TaskResponse) 
def modify_task(task_id: int, updated_data: TaskUpdate, db: Session = Depends(get_db)):
  db_task = get_task_by_id(db, task_id=task_id)
  if db_task is None:
    raise HTTPException(status_code=404, detail="Task not found")
  
  return update_task(
    db=db,
    db_task=db_task,
    title=updated_data.title,
    description=updated_data.description,
    completed=updated_data.is_completed
  )

@router.delete("/task/{task_id}", response_model=TaskResponse)
def remove_task(task_id: int, db: Session =  Depends(get_db)):
  db_task = get_task_by_id(db, task_id=task_id)
  if db_task is None:
    raise HTTPException(status_code=404, detail="Task not found")
  delete_task(db, db_task=db_task)
  # Here i send a 204 response, no content, meaning success but i don't send the data back
  return Response(status_code=204)