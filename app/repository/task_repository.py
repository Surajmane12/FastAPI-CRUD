

from typing import List

from sqlalchemy import select

from app.models.task import Task
from app.schemas.task import TaskCreate,TaskRead, TaskUpdate
from sqlalchemy.orm import Session

def create_task(db:Session,task_data:TaskCreate)->Task:
    task = Task(**task_data.model_dump())
    # model_dump -> converts the model type into dictionary type
    # The above is the instance of your SQLAlchemy Task class.
    # Similar to the belowed line: 
    # task = Task(
    #     title="Learn FastAPI",
    #     description="Understand SQLAlchemy"
    # )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_all_tasks(db:Session)->List[Task]:
    query=select(Task).order_by(Task.id)
    return list(db.scalars(query).all())

def get_task_by_id(db:Session,task_id:int)->Task | None:
    query = select(Task).where(Task.id==task_id)
    return db.scalars(query).one_or_none()

def update_task(db:Session,task:Task,taskdata:TaskUpdate)->Task | None:
    for field,value in taskdata.model_dump().items():
        setattr(task,field,value)
        db.commit()
        db.refresh(task)
        return task

def delete_task(db:Session,task:Task)->None:
    db.delete(task)
    db.commit()