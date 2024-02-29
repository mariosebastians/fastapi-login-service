from db.database import get_db, db_dependency
from db.models import Users, Roles
from handler import exception
from handler.auth import ctx, authenticate_user, create_token
from schema import Token

from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

def create_user(username: str, password: str, role_id: int, db: db_dependency):
    if db.query(Users).filter(Users.username == username).first():
        exception.account_is_already_exist(username)
    if role_id < 1 or role_id > 2:
        exception.roles_is_not_available()
    new_user = Users(
        username = username,
        password = ctx.hash(password),
        role_id = role_id
    )
    db.add(new_user)
    db.commit()
    return "Successfully create account!"

def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        exception.user_not_found()
    token = create_token(user.id, user.username, user.role_id)
    
    return Token(
        access_token = token,
        token_type = 'bearer'
    )
    
def get_all_user(db: Session = Depends(get_db)):
    result = db.query(Users, Roles.role_name).join(Roles).filter(Users.role_id == Roles.role_id).all()
    return [{"user_id": user.id, "username": user.username, "password": user.password, "role_name": role_name} for user, role_name in result]
    
