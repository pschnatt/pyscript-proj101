from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction
from pydantic import BaseModel

# Open the database
storage = FileStorage("workout_database.fs")
db = DB(storage)
connection = db.open()
root = connection.root()

# Define Workout model as a Pydantic model
class Workout(BaseModel):
    name: str
    reps: int
    sets: int

# Dependency to get the ZODB root for each request
def get_db():
    return root

# Function to commit transactions
def commit_transaction():
    transaction.commit()

# Close the connection when the app is shutting down
def close_db_connection():
    connection.close()
