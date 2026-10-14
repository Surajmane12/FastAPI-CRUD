

from fastapi import HTTPException,status
from requests import Session

from app.schemas.users import UserCreate, UserLogin
from app.repository import auth_repository

def register_user(db:Session,user_data:UserCreate):
    user = auth_repository.validate_user(db,user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email ID is already registered!!"
        )
    return auth_repository.register_user(db,user_data)

def login_user(db:Session,user_data:UserLogin)->dict:
    if not user_data.identifier.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ID OR Username field is missing!!"
        )
    return auth_repository.login_user(db,user_data)
