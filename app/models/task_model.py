from app.settings.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from uuid import uuid4

class TaskOrm(Base):
    __tablename__ = 'Task'

    id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        primary_key=True,
        default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(
        nullable=False,
        default='CREATED')