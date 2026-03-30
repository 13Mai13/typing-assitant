"""Lessons API router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Lesson, LessonProgress
from app.schemas.lesson import (
    GenerateTextRequest,
    GenerateTextResponse,
    LessonResponse,
    LessonWithProgress,
)
from app.services.lesson_generator import generate_practice_text

router = APIRouter()


@router.get("/lessons", response_model=list[LessonWithProgress])
async def get_all_lessons(db: Session = Depends(get_db)):
    """Get all lessons with user progress.

    Returns lessons ordered by position with progress information.
    If no progress exists for a lesson, default values are used.
    """
    lessons = db.query(Lesson).order_by(Lesson.position).all()

    # Get all progress records
    progress_records = {p.lesson_id: p for p in db.query(LessonProgress).all()}

    # Combine lessons with progress
    result = []
    for lesson in lessons:
        progress = progress_records.get(lesson.id)

        lesson_data = LessonWithProgress(
            id=lesson.id,
            name=lesson.name,
            description=lesson.description,
            unlocked_keys=lesson.get_unlocked_keys_list(),
            difficulty_level=lesson.difficulty_level,
            required_confidence=lesson.required_confidence,
            required_wpm=lesson.required_wpm,
            required_accuracy=lesson.required_accuracy,
            position=lesson.position,
            is_unlocked=progress.is_unlocked if progress else (lesson.position == 1),
            is_completed=progress.is_completed if progress else False,
            current_confidence=progress.current_confidence if progress else 0.0,
            best_wpm=progress.best_wpm if progress else None,
            best_accuracy=progress.best_accuracy if progress else None,
            attempts=progress.attempts if progress else 0,
        )
        result.append(lesson_data)

    return result


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Get a specific lesson by ID."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return LessonResponse(
        id=lesson.id,
        name=lesson.name,
        description=lesson.description,
        unlocked_keys=lesson.get_unlocked_keys_list(),
        difficulty_level=lesson.difficulty_level,
        required_confidence=lesson.required_confidence,
        required_wpm=lesson.required_wpm,
        required_accuracy=lesson.required_accuracy,
        position=lesson.position,
    )


@router.post("/lessons/{lesson_id}/generate-text", response_model=GenerateTextResponse)
async def generate_lesson_text(
    lesson_id: int,
    request: GenerateTextRequest,
    db: Session = Depends(get_db),
):
    """Generate practice text for a specific lesson.

    Generates pseudo-words using the lesson's unlocked keys.
    Optionally emphasizes weak keys if provided.
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    available_keys = lesson.get_unlocked_keys_list()

    # Generate practice text
    text = generate_practice_text(
        available_keys=available_keys,
        word_count=request.word_count,
        weak_keys=request.weak_keys,
    )

    return GenerateTextResponse(
        text=text,
        word_count=len(text.split()),
        available_keys=available_keys,
    )
