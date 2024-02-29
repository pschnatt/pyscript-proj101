import persistent
from pydantic import BaseModel
from abc import ABC, abstractmethod


class Account(ABC):
    def __init__(self, username, password, hashed_password=""):
        self.username = username
        self.password = password
        self.hashed_password = hashed_password


class User(Account, persistent.Persistent):
    def __init__(
        self,
        username,
        password,
        hashed_password="",
        height=0,
        weight=0,
        workouts=[],
        meals = [],
    ):
        Account.__init__(self, username, password, hashed_password)
        self.height = height
        self.weight = weight
        self.workouts = persistent.list.PersistentList(workouts)
        self.meals = persistent.list.PersistentList(meals)


    def log_workout(self, workout):
        self.workouts.append(workout)

    def view_workout_history(self):
        return self.workouts

    def track_progress(self):
        pass

    def set_goal(self, goal):
        pass

    def view_meal_plan(self):
        return self.meals


class Trainer(Account, persistent.Persistent):
    def __init__(self, username, password, hashed_password="", specialty="", clients=[]):
        Account.__init__(self, username, password, hashed_password)
        self.specialty = specialty
        self.clients = persistent.list.PersistentList(clients)

    def create_workout_plan(self, user, plan):
        pass

    def track_client_progress(self, user):
        pass

    def suggest_diet_plan(self, user):
        pass


class Workout(persistent.Persistent):
    def __init__(self, name, exercises=[]):
        self.name = name
        self.exercises = persistent.list.PersistentList(exercises)
        self.editable = True

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def remove_exercise(self, exercise):
        if exercise in self.exercises:
            self.exercises.remove(exercise)

    def view_exercises(self):
        return self.exercises


class Exercise(persistent.Persistent):
    def __init__(self, name, category, sets, reps, weight=0):
        self.name = name
        self.category = category
        self.sets = sets
        self.reps = reps
        self.weight = weight
    


class DietPlan(persistent.Persistent):
    def __init__(self, date, meals=[]):
        self.date = date
        self.meals = persistent.list.PersistentList(meals)

    def add_meal(self, meal):
        self.meals.append(meal)

    def remove_meal(self, meal):
        if meal in self.meals:
            self.meals.remove(meal)

    def view_meals(self):
        return self.meals


class Meal(persistent.Persistent):
    def __init__(self, name, calories, protein, carbs, fats, ingredients=[]):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fats = fats
        self.ingredients = persistent.list.PersistentList(ingredients)


# class Nutritionist(Account, persistent.Persistent):
#     def __init__(self, username, password, hashed_password="", clients=[]):
#         Account.__init__(self, username, password, hashed_password)
#         self.clients = persistent.list.PersistentList(clients)

#     def create_diet_plan(self, user, plan):
#         pass

#     def track_client_nutrition(self, user):
#         pass

#     def suggest_supplements(self, user):
#         pass
