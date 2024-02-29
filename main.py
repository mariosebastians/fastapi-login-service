from db import repository
from db.database import db_dependency
from handler.auth import admin_dependency

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

@app.post("/login", tags=["Public"], summary="Do a login and retreive a JWT Token")
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return repository.login_user(form_data, db)

@app.get("/users", tags=["Admin Only"], summary="Retrieve all user data", 
         description="You will need to authenticate using an Admin account to access this endpoint")
def get_all_user(admin: admin_dependency, db: db_dependency):
    return repository.get_all_user(db)