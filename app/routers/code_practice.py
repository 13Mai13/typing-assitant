"""Code practice API router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CodeProblem

router = APIRouter()


@router.get("/code/problems")
async def get_code_problems(language: str | None = None, db: Session = Depends(get_db)):
    """Get all code problems, optionally filtered by language.

    Args:
        language: Optional language filter (python, rust, typescript)
        db: Database session

    Returns:
        List of code problems
    """
    query = db.query(CodeProblem)

    if language:
        query = query.filter(CodeProblem.language == language)

    problems = query.all()

    return [
        {
            "id": p.id,
            "problem_id": p.problem_id,
            "title": p.title,
            "language": p.language,
            "difficulty": p.difficulty,
            "category": p.category,
        }
        for p in problems
    ]


@router.get("/code/problems/{problem_id}")
async def get_code_problem(problem_id: str, db: Session = Depends(get_db)):
    """Get a specific code problem by ID.

    Args:
        problem_id: Problem identifier
        db: Database session

    Returns:
        Full problem details including code content
    """
    problem = db.query(CodeProblem).filter(CodeProblem.problem_id == problem_id).first()

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    return {
        "id": problem.id,
        "problem_id": problem.problem_id,
        "title": problem.title,
        "language": problem.language,
        "difficulty": problem.difficulty,
        "category": problem.category,
        "content": problem.content,
    }
