

from fastapi import HTTPException,status


from app.schemas.users import UserCreate, UserLogin, UserRead
from app.repository import auth_repository
from app.core.security import verify_password, create_access_token
from app.core.exceptions import CustomException

def register_user(user_data:UserCreate)->UserRead:
    user = auth_repository.validate_user(user_data.email)
    print("User Validated: ",user)
    print("User Data: ",user_data)
    if user:
        CustomException.call(
            message="Email Id Already Registered!!",
            status_code=status.HTTP_409_CONFLICT
        )
    return auth_repository.create(user_data)

def login_user(user_data:UserLogin)->dict:
    if not user_data.identifier.strip():
        CustomException.call(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Email ID OR Username field is missing!!"
        )
    user = auth_repository.read(user_data)
    if user is None:
        CustomException.call(
            message="Invalid username or email!",
            status_code=status.HTTP_401_UNAUTHORIZED,
            exception_type=ValueError,
        )
    elif not verify_password(user_data.password,user.password):
        CustomException.call(
            message="Invalid Password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    access_token = create_access_token(user.id)

    return {
        "user":{
            "id":user.id,
            "username":user.username,
            "email":user.email
        },
        "access_token":access_token
    }
    
