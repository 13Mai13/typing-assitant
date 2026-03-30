"""Per-key performance statistics database model."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class KeyStatistics(Base):
    """Tracks performance statistics for individual keys."""

    __tablename__ = "key_statistics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key_char: Mapped[str] = mapped_column(String(1), nullable=False)
    keyboard_layout: Mapped[str] = mapped_column(String(50), nullable=False)

    # Aggregate stats
    total_presses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    correct_presses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    incorrect_presses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Timing (in milliseconds)
    avg_press_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    min_press_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_press_time: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Confidence scoring (0.0 to 1.0)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    __table_args__ = (
        UniqueConstraint("key_char", "keyboard_layout", name="uq_key_statistics_key_layout"),
    )
