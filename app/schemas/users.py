
from pydantic import BaseModel, ConfigDict, EmailStr,Field,field_validator, model_validator
import re

from app.schemas.usersummary import UserSummary

class UserCreate(BaseModel):
    username:str=Field(min_length=2,max_length=20)
    email:EmailStr=Field(min_length=2,max_length=30)
    password:str=Field(min_length=5,max_length=20)

    @field_validator("username",mode="before")
    @classmethod
    def normalize_username(cls,value:str)->str:
        if not isinstance(value,str):
            raise ValueError("Username must be a string!!")
        return value.strip().lower()

    @field_validator("username",mode="before")
    @classmethod
    def validate_username(cls,value:str)->str:
        if not re.fullmatch(r"[a-z][a-z0-9_]*", value):
            raise ValueError("Username must start with letter and contain only letters, numbers and underscores..")
        return value

    # Password Custom Validations
    @field_validator("password",mode="before")
    @classmethod
    def validate_password(cls,value:str)->str:
        if value!=value.strip():
            raise ValueError("Password must not contains the whitespaces")
        if not re.search(r"[a-z]",value):
            raise ValueError("Password must contains atleast one lowecase character")
        if not re.search(r"[A-Z]",value):
            raise ValueError("Password must contains atleast one Uppercase character")
        if not re.search(r"\d",value):
            raise ValueError("Password must contains atleast one numberic character")
        if not re.search(r"[^a-zA-Z0-9\s]",value):
            raise ValueError("Password must contains atleast one special character")
        return value
        
class UserRead(BaseModel):
    id:int
    username:str
    email:EmailStr
    isactive:bool
    users:UserSummary
    
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    identifier:str | None=None
    password: str = Field(min_length=5, max_length=20)

    @model_validator(mode="after")
    def validate_login_identifier(self):
        if not self.identifier:
            raise ValueError("Either username or email is required")

        return self

model_config=ConfigDict(from_attributes=True)

