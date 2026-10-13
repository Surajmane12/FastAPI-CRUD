
from typing import List

from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session
from app.models.task import Task
from app.repository import task_repository

def create_task(db:Session,task_data:TaskCreate)->Task:
    return task_repository.create_task(db,task_data)

def get_tasks(db:Session)->List[Task]:
    return task_repository.get_all_tasks(db)

def get_task_by_id(db:Session,task_id:int)->Task:
    return task_repository.get_task_by_id(db,task_id)

def update_task(db:Session,task_id:int,taskdata:TaskUpdate)->Task | None:
    
    task = task_repository.get_task_by_id(db,task_id)

    if task is None:
        return None
    
    return task_repository.update_task(db,task,taskdata)

def delete_task(db:Session,task_id:int)->bool:
   task = task_repository.get_task_by_id(db,task_id)
   if task is None:
       return False
   task_repository.delete_task(db,task)
   return True
    