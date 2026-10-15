from sqlalchemy import Boolean, DateTime, ForeignKey, Integer,String,func
from sqlalchemy.orm import Mapped,mapped_column, relationship
from datetime import datetime
from app.db.base import Base
from typing import TYPE_CHECKING

from app.models.taskassignments import TaskAssignments
if TYPE_CHECKING:
    from app.models.user import User

class Task(Base):

    __tablename__="tasks"

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
        String(500),
        nullable=False,
        default=""
    )
    completed:Mapped[bool]=mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    created_At:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    assignments: Mapped[list["TaskAssignments"]] = relationship(
        "TaskAssignments",
        back_populates="task",
        cascade="all, delete-orphan",
    )

    @property
    def assigned_user(self):
        return [assignment.user for assignment in self.assignments]
    