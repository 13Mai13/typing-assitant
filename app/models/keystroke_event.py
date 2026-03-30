"""Keystroke event database model for detailed tracking."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class KeystrokeEvent(Base):
    """Detailed keystroke tracking for analysis."""

    __tablename__ = "keystroke_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("sessions.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    key_pressed: Mapped[str] = mapped_column(String(1), nullable=False)
    expected_key: Mapped[str] = mapped_column(String(1), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    press_duration_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
