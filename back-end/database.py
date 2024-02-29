import ZODB, ZODB.FileStorage
import transaction
import BTrees
import atexit
from models import *

storage = ZODB.FileStorage.FileStorage("mydata.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root


def init_db():
    global root
    print("Initializing database.")
    try:
        if not hasattr(root, "users"):
            root.users = BTrees.OOBTree.BTree()
            # Adding default users
            root.users["user1"] = User("user1", "password1")
            root.users["user2"] = User("user2", "password2")
            root.users["user3"] = User("user3", "password3")

        if not hasattr(root, "trainers"):
            root.trainers = BTrees.OOBTree.BTree()
            # Adding default trainers
            root.trainers["trainer1"] = Trainer("t1", "tpassword1")
            root.trainers["trainer2"] = Trainer("t2", "tpassword2")

        if not hasattr(root, "exerciseList"):
            root.exerciselist = BTrees.OOBTree.BTree()
            root.exerciselist["Benchpress"] = Exercise("Bench press", "Bodybuilding", 4, 12, 225)
            root.exerciselist["Squat"] = Exercise("Squat", "Bodybuilding", 4, 10, 315)
            root.exerciselist["Deadlift"] = Exercise("Deadlift", "Bodybuilding", 4, 8, 405)

        if not hasattr(root, "meallist"):
            root.meallist = BTrees.OOBTree.BTree()
            root.meallist["Food1"] = Meal("Food1",250,30,120,8,["ingre1", "ingre2"])
            root.meallist["Food2"] = Meal("Food2",850,22,450,12,["ingre3", "ingre4"])
            root.meallist["Food3"] = Meal("Food3",1050,15,750,8,["ingre5", "ingre6"])
        print("Database loaded from file.")
        
    except Exception as e:
        print("Error loading database from file:", e)
        print("Initializing database with default data.")
        root.users = BTrees.OOBTree.BTree()
        root.trainers = BTrees.OOBTree.BTree()
        root.exerciselist = BTrees.OOBTree.BTree()
        root.meallist = BTrees.OOBTree.BTree()

# user CRUD

def create_user(username, password, height, weight, workouts=None, meals=None):
    if not workouts:
        workouts = []
    if not meals:
        meals = []
    if username in connection.root.users:
        raise ValueError("Username already exists. Please choose a different username.")
    
    user = User(username, password, height=height, weight=weight, workouts=workouts, meals=meals)
    connection.root.users[username] = user
    transaction.commit()

def update_user(username, new_data):
    user = connection.root.users.get(username)
    if user:
        for key, value in new_data.items():
            if value is not None:
                setattr(user, key, value)
        transaction.commit()
    else:
        print(f"User '{username}' not found.")

def delete_user(username):
    user = connection.root.users.pop(username, None)
    if user:
        transaction.commit()
        print(f"User '{username}' deleted.")
    else:
        print(f"User '{username}' not found.")

def fetch_users(username=None):
    users = connection.root.users.values()
    if username:
        user = connection.root.users.get(username)
        return [user] if user else []
    return list(users)

def close_db_connection():
    global connection, db
    transaction.commit()
    connection.close()
    db.close()
    print("Database closed.")

atexit.register(close_db_connection)