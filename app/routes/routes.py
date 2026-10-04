from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import dbConnection
from app.schemas import schema
from app.database import crud

router = APIRouter(prefix="/user", tags=["tasks"])
  
@router.post("/task/add", response_model=schema.TaskResponse, status_code=201)
async def create_new_task(task: schema.TaskCreate, db: Session = Depends(dbConnection.get_db)):
  return crud.create_task(db=db, task=task)

@router.get("/task/")
async def view_task():
  return {}

@router.put("/task/change") 
async def change_task():
  return {}

@router.delete("/task/delete")
async def delete_task():
  return {}