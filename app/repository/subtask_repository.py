from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import sessionLocal
from app.models.task import Task
from app.models.user import User
from app.models.taskassignments import TaskAssignments
from app.models.subtask import SubTasks
from app.schemas.subtask import Create,SubTaskUpdate



def read_by_id(id: int) -> Task | None:
    with sessionLocal() as db:
        query = (
            select(SubTasks)
            .where(SubTasks.id == id)
        )

        return db.scalar(query)


def create(subtask_data: Create) -> SubTasks:
    with sessionLocal.begin() as db:
        # 1. Verify that the parent task exists
        
        parent_task = db.get(Task, subtask_data.task_id)

        if parent_task is None:
            raise ValueError("Parent task does not exist.")

        # 2. Get unique assigned user IDs
        user_ids = set(subtask_data.assigned_user_ids)

        # 3. Fetch users from the database
        users = list(
            db.scalars(
                select(User).where(User.id.in_(user_ids))
            ).all()
        )

        # 4. Validate that all requested users exist
        if len(users) != len(user_ids):
            raise ValueError("One or more assigned users do not exist.")

        # 5. Create the subtask without the assignment-only field
        subtask = SubTasks(
        **subtask_data.model_dump(
        exclude={"assigned_user_ids", "task_id"}
        ),
    task_id=subtask_data.task_id,
)
        # 6. Create assignments for this subtask
        subtask.assignments = [
            TaskAssignments(user=user)
            for user in users
        ]

        db.add(subtask)

        # 7. Insert the subtask to generate its ID
        db.flush()

        # 8. Fetch the subtask with its assigned users loaded
        query = (
            select(SubTasks)
            .options(
                selectinload(SubTasks.assignments)
                .selectinload(TaskAssignments.user)
            )
            .where(SubTasks.id == subtask.id)
        )

        return db.scalar(query)


def update(id: int, subtask_data: SubTaskUpdate) -> SubTasks:
    with sessionLocal.begin() as db:
        # 1. Find the subtask
        subtask = db.get(SubTasks, id)

        if subtask is None:
            raise ValueError("Subtask not found.")

        # 2. Get only the fields provided by the client
        data = subtask_data.model_dump(exclude_unset=True)

        # 3. Extract assignment IDs separately
        user_ids = data.pop("assigned_user_ids", None)

        # 4. Update regular subtask fields
        for field, value in data.items():
            setattr(subtask, field, value)

        # 5. Update assigned users only if the field was provided
        if user_ids is not None:
            user_ids = set(user_ids)

            users = list(
                db.scalars(
                    select(User).where(User.id.in_(user_ids))
                ).all()
            )

            if len(users) != len(user_ids):
                raise ValueError("One or more assigned users do not exist.")

            # Remove assignments for users no longer selected
            subtask.assignments[:] = [
                assignment
                for assignment in subtask.assignments
                if assignment.user_id in user_ids
            ]

            # Keep existing assignments and add newly selected users
            existing_user_ids = {
                assignment.user_id
                for assignment in subtask.assignments
            }

            for user in users:
                if user.id not in existing_user_ids:
                    subtask.assignments.append(
                        TaskAssignments(
                            task_id=subtask.task_id,
                            user=user,
                        )
                    )

        # 6. Flush changes before fetching the updated object
        db.flush()

        # 7. Reload relationships required by the response schema
        query = (
            select(SubTasks)
            .options(
                selectinload(SubTasks.assignments)
                .selectinload(TaskAssignments.user)
            )
            .where(SubTasks.id == id)
        )

        return db.scalar(query)


