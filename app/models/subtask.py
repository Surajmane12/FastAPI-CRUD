from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.taskassignments import TaskAssignments


class SubTasks(Base):
    __tablename__="subtasks"

    id:Mapped[int]=mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    title:Mapped[str]=mapped_column(
        String(200),
        nullable=False
    )
    description:Mapped[str]=mapped_column(
        String(300),
        nullable=True,
        default="not provided"
    )
    completed:Mapped[bool]=mapped_column(
            Boolean,
            nullable=False,
            default=False
    )
    task_id:Mapped[int]=mapped_column(
        Integer,
        ForeignKey("tasks.id",ondelete="CASCADE"),
        nullable=False
    )
    # Building Relationship 

    task:Mapped["Task"]=relationship(
        "Task",
        back_populates="subtasks"
    )

    assignments:Mapped[list["TaskAssignments"]]=relationship(
        "TaskAssignments",
        back_populates="sub_task",
        cascade="all, delete-orphan"
    )

    @property
    def assigned_user(self):
        return [assignment.user for assignment in self.assignments]