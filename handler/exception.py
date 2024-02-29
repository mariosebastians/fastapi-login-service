from fastapi import HTTPException, status

def roles_is_not_available():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please select existing roles, 1 for Admin & 2 for Public")

def account_is_already_exist(username: str):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Account with username '{username}' is already exist")

def user_not_found():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or credential might be incorrect")

def couldnt_validate_user():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't validate user")

def UserIsNotAdmin(username: str):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User '{username}', is not an Admin Account")