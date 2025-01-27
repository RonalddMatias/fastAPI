from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI() # Create an instance of FastAPI

# Base Model
class User(BaseModel):
    id: int
    name: str
    age: int
    email: str

# List of Users
users_db: List[User] = []

# Get all users
@app.get("/usersgetall", response_model=List[User])
def get_all_users():
    """Return all users that are stored in the database"""
    return users_db

# Get a user by id
@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user 
    raise HTTPException(status_code=404, detail="User not found") 

@app.post("/users", response_model=User, status_code=200)
def create_user(user: User):
    for i in users_db:
        if i.id == user.id:
            raise HTTPException(status_code=400, detail="ID already exists")
    users_db.append(user)
    return user

@app.put("/users/{user_id}", response_model=User, status_code=200)
def update_user(user_id:int, user: User):
    for user in users_db:
        if user.id == user_id:
            user.name = user.name
            user.age = user.age
            user.email = user.email
            return user
    

@app.delete("/users/{user_id}", response_model=str, status_code=200)
def delete_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            users_db.remove(user)
            return "User deleted successfully"
    raise HTTPException(status_code=404, detail="User not found")

