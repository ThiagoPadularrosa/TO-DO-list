from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.dbConnection import Base

class TaskModel(Base):
  __tablename__ = "tasks"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  title: Mapped[Optional[str]] = mapped_column(String(100))
  description: Mapped[Optional[str]] = mapped_column(String(255))
  is_completed: Mapped[Optional[bool]] = mapped_column(default=False)