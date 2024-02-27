from fastapi import FastAPI
from typing import List
from models import User
f
app = FastAPI()


@app.get("/")
async def root():
  return {"msg":"Hello"}

@app.get("/workout")
async def fetch_workouts():
  return