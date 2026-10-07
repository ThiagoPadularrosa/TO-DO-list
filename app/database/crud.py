from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.models import TaskModel
from app.schemas.schema import TaskCreate, TaskUpdate
import pymysql

def create_task(db: Session, task: TaskCreate ):
  db_task = TaskModel(
      title=task.title,
      description=task.description
  )
  db.add(db_task)
  db.commit()
  db.refresh(db_task) # Loads the generated ID from the database
  return db_task

def get_task_by_id(db: Session, task_id: int):
  return db.query(TaskModel).filter(TaskModel.id == task_id).first()

def get_all_tasks(db: Session, skip: int, limit: int = 100):
  return db.query(TaskModel).offset(skip).limit(limit).all()

def update_task(db: Session, db_task: TaskUpdate, title: str, description: str | None, completed: bool):
  db_task.title = title
  db_task.description = description
  db_task.is_completed = completed
  try:
    db.commit()
    db.refresh(db_task)
  except IntegrityError as e:
    db.rollback()
    if isinstance(e.orig, pymysql.err.OperationalError) or isinstance(e.orig, pymysql.err.IntegrityError):
      if e.orig.args[0] == 1062:
        print("¡Error: Duplicated entry (Unique constraint violated)!")
      else:
        print(f"Another integrity error of MySQL: {e.orig}")
  return db_task

def delete_task(db: Session, db_task: TaskModel):
  db.delete(db_task)
  db.commit()
  return True