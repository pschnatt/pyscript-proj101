from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import get_db, commit_transaction, close_db_connection, Workout, DB
from typing import List

app = FastAPI()

# Model for creating a workout
class WorkoutCreate(BaseModel):
    name: str
    reps: int
    sets: int

# Create a new workout
@app.post("/workouts/", response_model=Workout)
def create_workout(workout: WorkoutCreate, db: DB = Depends(get_db)):
    # Check if workout with the same name already exists
    if workout.name in db:
        raise HTTPException(status_code=400, detail="Workout with this name already exists")

    # Store the workout in the database
    db[workout.name] = Workout(name=workout.name, reps=workout.reps, sets=workout.sets)
    commit_transaction()

    return db[workout.name]

# Get all workouts
@app.get("/workouts/", response_model=List[Workout])
def get_workouts(db: DB = Depends(get_db)):
    return list(db.values())

# Get a specific workout by name
@app.get("/workouts/{workout_name}", response_model=Workout)
def get_workout(workout_name: str, db: DB = Depends(get_db)):
    workout = db.get(workout_name)
    if workout:
        return workout
    else:
        raise HTTPException(status_code=404, detail="Workout not found")

# Update a workout by name
@app.put("/workouts/{workout_name}", response_model=Workout)
def update_workout(workout_name: str, updated_workout: WorkoutCreate, db: DB = Depends(get_db)):
    existing_workout = db.get(workout_name)
    if not existing_workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    # Update the existing workout
    existing_workout.name = updated_workout.name
    existing_workout.reps = updated_workout.reps
    existing_workout.sets = updated_workout.sets

    commit_transaction()

    return existing_workout

# Delete a workout by name
@app.delete("/workouts/{workout_name}", response_model=Workout)
def delete_workout(workout_name: str, db: DB = Depends(get_db)):
    workout = db.pop(workout_name, None)
    if workout:
        commit_transaction()
        return workout
    else:
        raise HTTPException(status_code=404, detail="Workout not found")

# Event to close the connection when the app is shutting down
@app.on_event("shutdown")
def close_db_connection_on_shutdown():
    close_db_connection()
