"""Typing session database model."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Session(Base):
    """Records each typing practice session."""

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    mode: Mapped[str] = mapped_column(String(20), nullable=False)  # 'lesson', 'custom', 'code'
    lesson_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("lessons.id"), nullable=True)
    keyboard_layout: Mapped[str] = mapped_column(String(50), nullable=False)

    # Metrics
    total_keystrokes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    correct_keystrokes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    incorrect_keystrokes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duration_seconds: Mapped[float] = mapped_column(Float, nullable=False)

    # Calculated metrics
    gross_wpm: Mapped[float | None] = mapped_column(Float, nullable=True)
    net_wpm: Mapped[float | None] = mapped_column(Float, nullable=True)
    accuracy: Mapped[float | None] = mapped_column(Float, nullable=True)

    # For code practice
    language: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # 'python', 'rust', 'typescript'
    problem_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
