from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from .database import engine
from .routers import post, user, auth, vote
from pydantic_settings import BaseSettings

# All necessary imports for auth are present via .routers.auth
# (auth.py itself imports: status, HTTPException, Depends, APIRouter, responses, models, schemas, utils, get_db, Session)

#models.Base.metadata.create_all(bind=engine) #command which tells sqlalchemy to create all the tables in the database



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], #allows all headers (Content-Type, Authorization, etc.)
)

app.include_router(post.router)  # include_router is used to include the router in the main file
app.include_router(user.router)  # include_router is used to include the router in the main file
app.include_router(auth.router)  # include_router is used to include the router in the main file
app.include_router(vote.router)  # include_router is used to include the router in the main file

@app.get("/")
async def read_root():
    return {"Hello": "Welcome to my API !!!!!"}
