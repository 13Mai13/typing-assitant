"""Lesson database model."""

import json

from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Lesson(Base):
    """Represents a typing lesson with specific keys to practice."""

    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    unlocked_keys: Mapped[str] = mapped_column(Text, nullable=False)  # JSON array: ["a", "s", "d"]
    difficulty_level: Mapped[int] = mapped_column(Integer, nullable=False)
    required_confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    required_wpm: Mapped[float] = mapped_column(Float, nullable=False, default=35.0)
    required_accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    position: Mapped[int] = mapped_column(Integer, nullable=False)  # Order in progression

    def get_unlocked_keys_list(self) -> list[str]:
        """Parse unlocked_keys JSON into a list."""
        return json.loads(self.unlocked_keys)

    def set_unlocked_keys_list(self, keys: list[str]) -> None:
        """Set unlocked_keys from a list."""
        self.unlocked_keys = json.dumps(keys)
