"""Statistics API router."""

from fastapi import APIRouter, Depends
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import KeyStatistics, LessonProgress
from app.models import Session as TypingSession

router = APIRouter()


@router.get("/stats/overview")
async def get_stats_overview(db: Session = Depends(get_db)):
    """Get overview statistics.

    Returns:
        Overall statistics including total sessions, avg WPM, etc.
    """
    # Get session statistics
    total_sessions = db.query(TypingSession).count()

    # Get average WPM and accuracy
    avg_stats = db.query(
        func.avg(TypingSession.net_wpm).label("avg_wpm"),
        func.avg(TypingSession.accuracy).label("avg_accuracy"),
    ).first()

    # Get best scores
    best_wpm = db.query(func.max(TypingSession.net_wpm)).scalar() or 0
    best_accuracy = db.query(func.max(TypingSession.accuracy)).scalar() or 0

    # Get completed lessons
    completed_lessons = db.query(LessonProgress).filter(LessonProgress.is_completed).count()

    return {
        "total_sessions": total_sessions,
        "avg_wpm": round(avg_stats.avg_wpm or 0, 2),
        "avg_accuracy": round(avg_stats.avg_accuracy or 0, 2),
        "best_wpm": round(best_wpm, 2),
        "best_accuracy": round(best_accuracy, 2),
        "completed_lessons": completed_lessons,
    }


@router.get("/stats/sessions")
async def get_session_history(limit: int = 20, db: Session = Depends(get_db)):
    """Get recent typing sessions.

    Args:
        limit: Maximum number of sessions to return (default: 20)
        db: Database session

    Returns:
        List of recent typing sessions
    """
    sessions = db.query(TypingSession).order_by(desc(TypingSession.started_at)).limit(limit).all()

    return [
        {
            "id": s.id,
            "mode": s.mode,
            "started_at": s.started_at.isoformat(),
            "duration_seconds": s.duration_seconds,
            "net_wpm": round(s.net_wpm or 0, 2),
            "accuracy": round(s.accuracy or 0, 2),
            "total_keystrokes": s.total_keystrokes,
        }
        for s in sessions
    ]


@router.get("/stats/keys")
async def get_key_statistics(
    keyboard_layout: str = "macos_standard", db: Session = Depends(get_db)
):
    """Get per-key performance statistics.

    Args:
        keyboard_layout: Keyboard layout to get stats for
        db: Database session

    Returns:
        List of key statistics
    """
    key_stats = (
        db.query(KeyStatistics).filter(KeyStatistics.keyboard_layout == keyboard_layout).all()
    )

    return [
        {
            "key_char": k.key_char,
            "total_presses": k.total_presses,
            "correct_presses": k.correct_presses,
            "accuracy": round(
                (k.correct_presses / k.total_presses * 100) if k.total_presses > 0 else 0, 2
            ),
            "avg_press_time": round(k.avg_press_time or 0, 2),
            "confidence_score": round(k.confidence_score, 3),
        }
        for k in key_stats
    ]


@router.get("/stats/progress")
async def get_progress_over_time(db: Session = Depends(get_db)):
    """Get WPM and accuracy progress over time.

    Returns:
        Time series data for charts
    """
    # Get sessions ordered by date
    sessions = (
        db.query(TypingSession)
        .filter(TypingSession.ended_at.isnot(None))
        .order_by(TypingSession.started_at)
        .all()
    )

    return [
        {
            "date": s.started_at.date().isoformat(),
            "wpm": round(s.net_wpm or 0, 2),
            "accuracy": round(s.accuracy or 0, 2),
        }
        for s in sessions
    ]
