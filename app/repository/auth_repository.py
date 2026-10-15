


from typing import Annotated

from fastapi import Depends
from pydantic import EmailStr
from requests import Session
from sqlalchemy import Select, or_, select

from app.schemas.users import UserCreate, UserLogin, UserRead
from app.models.user import User
from app.core.security import hash_password
from app.db.session import sessionLocal


def validate_user(user_email:str)->User|None:
    with sessionLocal() as db:
        query = Select(User).where(User.email==user_email)
        return db.scalar(query)


def create(user_data:UserCreate)->User:
    with sessionLocal() as db:
        user=User(**user_data.model_dump(exclude={"password"}),
              password=hash_password(user_data.password),)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

def read(user_data:UserLogin)->dict:
    with sessionLocal() as db:
        query = select(User).where(
            or_(
                User.email == user_data.identifier,
                User.username == user_data.identifier,
            )
        )
        user=db.scalar(query)
        return user