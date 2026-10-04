from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import routes
from app.database.dbConnection import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
  # Startup logic goes here (e.g., connect to database)
  print('Starting up...')
  yield
  # Shutdown logic goes here (e.g., close connections)
  print('Shutting down...')

# I automatically create the tables in MySQL on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title= "Small api", lifespan=lifespan)

app.include_router(routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my small FastAPI todo app"}