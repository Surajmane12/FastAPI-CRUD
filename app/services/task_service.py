
from typing import List

from fastapi import HTTPException, logger, status
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session
from app.models.task import Task
from app.repository import task_repository
from app.core.exceptions import CustomException
from sqlalchemy.exc import SQLAlchemyError
import logging
logger = logging.getLogger(__name__)

def create_task(task_data: TaskCreate):
    try:
        return task_repository.create(task_data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except SQLAlchemyError as exc:
        logger.exception("Database error while creating task")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while creating the task.",
        ) from exc

    except Exception as exc:
        logger.exception("Unexpected error while creating task")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task.",
        ) from exc

        
def get_tasks()->List[Task]:
    task =  task_repository.read()
    if not task:
        CustomException.call(message="Empty Task List",status_code=status.HTTP_204_NO_CONTENT)
    return task

def get_task_by_id(task_id:int)->Task:
    task =  task_repository.read_by_id(task_id)
    if not task:
        CustomException.call(message="Empty Task List",status_code=status.HTTP_204_NO_CONTENT)
    return task

def update_task(task_id:int,taskdata:TaskUpdate)->Task | None:
    task = task_repository.read_by_id(task_id)
    if task is None:
        return None
    
    return task_repository.update(task,taskdata)

def delete_task(task_id:int)->bool:
   task = task_repository.read_by_id(task_id)
   if task is None:
       CustomException.call(
                  message="No Task Found",
                  status_code=status.HTTP_204_NO_CONTENT
              )
       return False
   task_repository.delete(task)
   return True
    