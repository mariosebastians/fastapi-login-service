from db.models import Users
from handler import exception

from typing import Annotated
from fastapi import Depends
from jose import jwt, JWTError
from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = '629182a40766c3e9aed88719defa299dbc0c097524ee7497ce91194c4ac60eec'
ALGORITHM = 'HS256'
TOKEN_EXPIRE_TIME = timedelta(minutes=10)

ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
auth = OAuth2PasswordBearer(tokenUrl='login')

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not ctx.verify(password, user.password):
        return False
    return user

def create_token(id: int, username: str, role_id: int):
    encode = {'sub': username, 'id': id, 'role_id': role_id}
    expire = datetime.utcnow() + TOKEN_EXPIRE_TIME
    encode.update({'exp': expire})
    encoded = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

def get_current_admin(token: Annotated[str, Depends(auth)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get('id')
        username: str = payload.get('sub')
        role_id: int = payload.get('role_id')
        if username is None or id is None:
            exception.couldnt_validate_user()
        if role_id == 2:
            exception.UserIsNotAdmin(username)
    except JWTError:
        exception.couldnt_validate_user()

admin_dependency = Annotated[dict, Depends(get_current_admin)]

# def get_current_user(token: Annotated[str, Depends(auth)]):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         id: int = payload.get('id')
#         username: str = payload.get('sub')
#         role_id: int = payload.get('role_id')
#         if username is None or id is None:
#             exception.couldnt_validate_user()
#     except JWTError:
#         exception.couldnt_validate_user()

# user_dependency = Annotated[dict, Depends(get_current_user)]



