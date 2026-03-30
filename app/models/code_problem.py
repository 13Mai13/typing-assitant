"""Code practice problem database model."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CodeProblem(Base):
    """Stores code practice problems for typing practice."""

    __tablename__ = "code_problems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    problem_id: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    language: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # 'python', 'rust', 'typescript'
    difficulty: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # 'easy', 'medium', 'hard'
    content: Mapped[str] = mapped_column(Text, nullable=False)  # The actual code to type
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    __table_args__ = (UniqueConstraint("problem_id", name="uq_code_problem_problem_id"),)
