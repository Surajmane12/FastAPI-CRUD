


from pydantic import EmailStr
from requests import Session
from sqlalchemy import Select, or_, select

from app.schemas.users import UserCreate, UserLogin, UserRead
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


def validate_user(db:Session,user_email:str)->User|None:
    query = Select(User).where(User.email==user_email)
    return db.scalar(query)


def register_user(db:Session,user_data:UserCreate)->User:
    user=User(**user_data.model_dump(exclude={"password"}),
              password=hash_password(user_data.password),)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db:Session,user_data:UserLogin)->dict:
    
    query = select(User).where(
        or_(
            User.email == user_data.identifier,
            User.username == user_data.identifier,
        )
    )
    
    user=db.scalar(query)

    if user is None:
        raise ValueError("Invalid username/email!!")
    if not verify_password(user_data.password,user.password):
        raise ValueError("Invalid password!!")
    access_token = create_access_token(user.id)

    return {
        "user":UserRead.model_validate(user).model_dump(),
        "access_token":access_token,
        "token_type":"Bearer"
    }



    