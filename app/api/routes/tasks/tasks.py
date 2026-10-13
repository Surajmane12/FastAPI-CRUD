from typing import Annotated, List

from fastapi import APIRouter, Depends,HTTPException,Request,Response,status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services import task_service
from app.models.task import Task

router=APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

DBSession = Annotated[Session,Depends(get_db)]

@router.post("",response_model=TaskRead,status_code=status.HTTP_201_CREATED)
def create_task(task_data:TaskCreate,db:DBSession):
    return task_service.create_task(db,task_data)

@router.get("",response_model=List[TaskRead])
def get_tasks(db:DBSession):
    return task_service.get_tasks(db)

@router.get("/{task_id}",response_model=TaskRead)
def get_tasks(db:DBSession,task_id:int):
    task = task_service.get_task_by_id(db,task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task Not Found")
    return task


@router.put("/{task_id}",response_model=TaskRead)
def update_task(db:DBSession,task_id:int,taskdata:TaskUpdate):
    return task_service.update_task(db,task_id,taskdata)

@router.delete("/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(db:DBSession,task_id:int):
    deleted = task_service.delete_task(db,task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)