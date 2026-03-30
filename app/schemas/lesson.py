"""Pydantic schemas for lesson-related API endpoints."""

from pydantic import BaseModel, Field


class LessonBase(BaseModel):
    """Base lesson schema."""

    name: str
    description: str | None = None
    unlocked_keys: list[str]
    difficulty_level: int
    required_confidence: float
    required_wpm: float
    required_accuracy: float
    position: int


class LessonResponse(LessonBase):
    """Lesson response schema with ID."""

    id: int

    class Config:
        from_attributes = True


class LessonWithProgress(LessonResponse):
    """Lesson with user progress information."""

    is_unlocked: bool = False
    is_completed: bool = False
    current_confidence: float = 0.0
    best_wpm: float | None = None
    best_accuracy: float | None = None
    attempts: int = 0


class GenerateTextRequest(BaseModel):
    """Request schema for generating practice text."""

    word_count: int = Field(default=50, ge=10, le=200)
    weak_keys: list[str] | None = None


class GenerateTextResponse(BaseModel):
    """Response schema for generated practice text."""

    text: str
    word_count: int
    available_keys: list[str]
