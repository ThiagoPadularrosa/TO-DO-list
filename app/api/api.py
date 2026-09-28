from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import userRoutes

@asynccontextmanager
async def lifespan(app: FastAPI):
  # Startup logic goes here (e.g., connect to database)
  print('Starting up...')
  yield
  # Shutdown logic goes here (e.g., close connections)
  print('Shutting down...')

app = FastAPI(title= "Small api", lifespan=lifespan)

app.include_router(userRoutes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my small FastAPI todo app"}