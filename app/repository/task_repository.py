
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import sessionLocal
from app.models.task import Task
from app.models.user import User
from app.models.taskassignments import TaskAssignments
from app.schemas.task import TaskCreate, TaskUpdate




def create(task_data: TaskCreate) -> Task:
    with sessionLocal.begin() as db:
        user_ids = set(task_data.assigned_user_ids)

        users = list(
            db.scalars(
                select(User).where(User.id.in_(user_ids))
            ).all()
        )

        if len(users) != len(user_ids):
            raise ValueError("One or more assigned users do not exist.")

        task = Task(
            **task_data.model_dump(exclude={"assigned_user_ids"})
        )

        task.assignments = [
            TaskAssignments(user=user)
            for user in users
        ]

        db.add(task)
        db.flush()

        query = (
            select(Task)
            .options(
                selectinload(Task.assignments)
                .selectinload(TaskAssignments.user)
            )
            .where(Task.id == task.id)
        )

        return db.scalar(query)
def read() -> list[Task]:
    with sessionLocal() as db:
        query = (
            select(Task)
            .options(
                selectinload(Task.assignments)
                .selectinload(TaskAssignments.user)
            )
            .order_by(Task.id)
        )

        return list(db.scalars(query).all())


def read_by_id(task_id: int) -> Task | None:
    with sessionLocal() as db:
        query = (
            select(Task)
            .options(
                selectinload(Task.assignments)
                .selectinload(TaskAssignments.user)
            )
            .where(Task.id == task_id)
        )

        return db.scalar(query)


def update(
    task_id: int,
    taskdata: TaskUpdate,
) -> Task | None:
    with sessionLocal() as db:
        try:
            task = db.get(Task, task_id)

            if task is None:
                return None

            data = taskdata.model_dump(exclude_unset=True)
            user_ids = data.pop("assigned_user_ids", None)

            for field, value in data.items():
                setattr(task, field, value)

            # Replace assignments only when provided
            if user_ids is not None:
                unique_ids = set(user_ids)

                users = list(
                    db.scalars(
                        select(User).where(User.id.in_(unique_ids))
                    ).all()
                )

                if len(users) != len(unique_ids):
                    raise ValueError(
                        "One or more assigned users do not exist."
                    )

                task.assignments = [
                    TaskAssignments(user=user)
                    for user in users
                ]

            db.commit()

            query = (
                select(Task)
                .options(
                    selectinload(Task.assignments)
                    .selectinload(TaskAssignments.user)
                )
                .where(Task.id == task_id)
            )

            return db.scalar(query)

        except Exception:
            db.rollback()
            raise


def delete(task_id: int) -> bool:
    with sessionLocal() as db:
        try:
            task = db.get(Task, task_id)

            if task is None:
                return False

            db.delete(task)
            db.commit()

            return True

        except Exception:
            db.rollback()
            raise
