from db.models import Users, Roles
from handler import exception
from handler.auth import ctx, authenticate_user, create_token, check_admin_role
from schema import Token

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

def get_user(username: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        exception.user_not_found()
    return user

def create_user(username: str, password: str, role_id: int, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if user:
        exception.account_is_already_exist()
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

def login_user(form_data: OAuth2PasswordRequestForm, db: Session):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        exception.user_not_found()
    token = create_token(user.id, user.username, user.role_id)
    
    return Token(
        access_token = token,
        token_type = 'bearer'
    )

def change_username(user: Users, new_name: str, db: Session):
    user.username = new_name
    db.commit()
    return f"Username is successfully changed"

def change_password(user: Users, old_pass: str, new_pass: str, db: Session):
    if not user:
        exception.user_not_found()
    if not ctx.verify(old_pass, user.password):
        exception.old_pass_is_incorrect()
    user.password = ctx.hash(new_pass)
    db.commit()
    return f"Password is successfully changed"

def get_all_user(admin: Users, db: Session):
    check_admin_role(admin)
    result = db.query(Users, Roles.role_name).join(Roles).filter(Users.role_id == Roles.role_id).all()
    return [{"user_id": user.id, "username": user.username, "password": user.password, "role_name": role_name} for user, role_name in result]

def delete_user(admin: Users, username: str, db: Session):
    check_admin_role(admin)
    user = get_user(username, db)
    db.delete(user)
    db.commit()
    return f"User with username '{username}' has been deleted successfully"