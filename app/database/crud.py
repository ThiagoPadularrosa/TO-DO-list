from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schema

def create_task(db: Session, task: schema.TaskCreate ):
  db_task = models.TaskModel(
      title=task.title,
      description=task.description
  )
  db.add(db_task)
  db.commit()
  db.refresh(db_task) # Loads the generated ID from the database
  return db_task