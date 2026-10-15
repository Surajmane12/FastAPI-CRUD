from typing import Annotated, List

from fastapi import APIRouter, Depends,HTTPException,Request,Response,status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import auth_service
from app.schemas.users import UserLogin, UserRead,UserCreate

router=APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("",response_model=UserRead,status_code=status.HTTP_201_CREATED)
def register_user(user_data:UserCreate)->UserRead:
    return auth_service.register_user(user_data)

@router.post("/login",response_model=dict,status_code=status.HTTP_200_OK)
def login_user(user_data:UserLogin)->dict:
    return auth_service.login_user(user_data)