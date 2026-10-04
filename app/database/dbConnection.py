import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

password = urllib.parse.quote_plus("40011@root+tato")

SQLALCHEMY_DATABASE_URL = (f"mysql+pymysql://root:{password}@localhost:3306/tato")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 

# Here i write the dependency to get the database session for each request
def get_db():
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()