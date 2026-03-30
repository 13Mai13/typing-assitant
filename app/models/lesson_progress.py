"""Lesson progress database model."""

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class LessonProgress(Base):
    """Tracks user's progress through lessons."""

    __tablename__ = "lesson_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lesson_id: Mapped[int] = mapped_column(Integer, ForeignKey("lessons.id"), nullable=False)
    current_confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    best_wpm: Mapped[float | None] = mapped_column(Float, nullable=True)
    best_accuracy: Mapped[float | None] = mapped_column(Float, nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_unlocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    __table_args__ = (UniqueConstraint("lesson_id", name="uq_lesson_progress_lesson_id"),)
