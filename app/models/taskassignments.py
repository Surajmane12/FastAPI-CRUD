
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.subtask import SubTasks

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User
    


class TaskAssignments(Base):
    __tablename__ = "taskassignments"

    __table_args__ = (
        # UniqueConstraint("task_id", "user_id", name="uq_task_user")
        UniqueConstraint("sub_task_id", "user_id", name="uq_subtask_user"),
        CheckConstraint(
            """
            (task_id IS NOT NULL AND sub_task_id IS NULL)
            OR
            (task_id IS NULL AND sub_task_id IS NOT NULL)
            """,
            name="ck_assignment_task_or_subtask",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    task_id: Mapped[int | None] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=True,
    )

    sub_task_id: Mapped[int | None] = mapped_column(
        ForeignKey("subtasks.id", ondelete="CASCADE"),
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    task: Mapped["Task | None"] = relationship(
        "Task",
        back_populates="assignments",
    )

    sub_task: Mapped["SubTasks | None"] = relationship(
        "SubTasks",
        back_populates="assignments",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="assignments",
    )
