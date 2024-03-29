from db import repository
from db.database import db_dependency
from schema import Token
from handler.auth import user_dependency

from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.post("/create", tags=["Public"], summary="Creates a new account")
def create_user(username: str, password: str, role_id: int, db: db_dependency):
    """
    Role list for role_id:
    - **1** for Admin role
    - **2** for Public role
    """
    return repository.create_user(username, password, role_id, db)

@app.post("/login", tags=["Public"], summary="Do a login and retreive a JWT Token", response_model=Token, include_in_schema=False)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return repository.login_user(form_data, db)

@app.put("/changename", tags=["Public"], summary="Change username")
def change_username(user: user_dependency, new_username: str, db: db_dependency):
    """
    You need to authenticate first in order to change your username    
    """
    return repository.change_username(user, new_username, db)

@app.put("/changepass", tags=["Public"], summary="Change user password")
def change_pass(user: user_dependency, old_pass: str, new_pass: str, db: db_dependency):
    """
    You need to authenticate first in order to change your password
    """
    return repository.change_password(user, old_pass, new_pass, db)

@app.get("/users", tags=["Admin Only"], summary="Retrieve all user data", 
         description="You will need to authenticate using an Admin account to access this endpoint")
def get_all_user(admin: user_dependency, db: db_dependency):
    return repository.get_all_user(admin, db)

@app.delete("/deleteuser", tags=["Admin Only"], summary="Delete a user by their username",
            description="You will need to authenticate using an Admin account to access this endpoint")
def delete_user(admin: user_dependency, username: str, db: db_dependency):
    return repository.delete_user(admin, username, db)
