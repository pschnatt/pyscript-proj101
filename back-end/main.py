from fastapi import FastAPI, Depends
from typing import List, Optional
from models import User
from database import *
from pydantic import BaseModel
app = FastAPI()


class Users(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None 
    height: Optional[float] = None 
    weight: Optional[float] = None


@app.post("/users")
async def create_user_route(user: Users):
    create_user(user.username, user.password, user.height, user.weight)
    return user

@app.put("/users/{username}")
async def update_user_route(username: str, updated_user: Users):
    update_user(username, updated_user.model_dump())
    return connection.root.users.get(username)

@app.delete("/users/{username}", response_model=None)
async def delete_user_route(username: str):
    deleted_user = connection.root.users.get(username)
    delete_user(username)
    return deleted_user

@app.get("/users/")
async def fetch_all_users():
    return fetch_users()

@app.get("/users/{username}")
async def fetch_user(username: str):
    return fetch_users(username)

init_db()