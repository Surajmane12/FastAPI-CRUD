from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class TaskCreate(BaseModel):
    title:str=Field(min_length=3,max_length=100)
    description:str=Field(default="",max_length=500)
    completed:bool=False

class TaskUpdate(BaseModel):
    title:str=Field(min_length=3,max_length=100)
    description:str=Field(default="",max_length=500)
    completed:bool=False

class TaskRead(BaseModel):
    id:int
    title:str
    description:str
    completed:bool
    created_At:datetime

model_config=ConfigDict(from_attribute=True)
