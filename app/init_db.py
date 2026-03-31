"""Database initialization script.

Run this script to create all tables and seed initial data:
    python -m app.init_db
"""

import json
from pathlib import Path

from app.config import settings
from app.database import Base, engine
from app.models import CodeProblem, Lesson


def init_db():
    """Create all database tables."""
    print(f"Creating database tables in {settings.database_url}...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")


def seed_lessons():
    """Seed initial lessons following keybr progression."""
    from app.database import SessionLocal

    db = SessionLocal()

    # Check if lessons already exist
    existing_count = db.query(Lesson).count()
    if existing_count > 0:
        print(f"✓ Lessons already seeded ({existing_count} lessons found)")
        db.close()
        return

    print("Seeding initial lessons...")

    lessons_data = [
        # Lesson 1: Start with home row basics
        {
            "name": "Home Row: F and J",
            "description": "Master the foundation keys with home row bumps",
            "unlocked_keys": json.dumps(["f", "j"]),
            "difficulty_level": 1,
            "position": 1,
            "required_confidence": 1.0,
            "required_wpm": 30.0,
            "required_accuracy": 0.95,
        },
        # Lesson 2: Expand home row
        {
            "name": "Home Row: D and K",
            "description": "Add the middle fingers",
            "unlocked_keys": json.dumps(["f", "j", "d", "k"]),
            "difficulty_level": 2,
            "position": 2,
            "required_confidence": 1.0,
            "required_wpm": 30.0,
            "required_accuracy": 0.95,
        },
        # Lesson 3: More home row
        {
            "name": "Home Row: S and L",
            "description": "Add the ring fingers",
            "unlocked_keys": json.dumps(["f", "j", "d", "k", "s", "l"]),
            "difficulty_level": 3,
            "position": 3,
            "required_confidence": 1.0,
            "required_wpm": 30.0,
            "required_accuracy": 0.95,
        },
        # Lesson 4: Complete home row
        {
            "name": "Complete Home Row",
            "description": "Master all home row keys",
            "unlocked_keys": json.dumps(["a", "s", "d", "f", "j", "k", "l", ";"]),
            "difficulty_level": 4,
            "position": 4,
            "required_confidence": 1.0,
            "required_wpm": 35.0,
            "required_accuracy": 0.95,
        },
        # Lesson 5: Start top row with most common letters
        {
            "name": "Top Row: E and I",
            "description": "Introduction to the top row with common vowels",
            "unlocked_keys": json.dumps(["a", "s", "d", "f", "j", "k", "l", ";", "e", "i"]),
            "difficulty_level": 5,
            "position": 5,
            "required_confidence": 1.0,
            "required_wpm": 35.0,
            "required_accuracy": 0.95,
        },
        # Lesson 6: More top row
        {
            "name": "Top Row: R and U",
            "description": "Continue with common consonants",
            "unlocked_keys": json.dumps(
                ["a", "s", "d", "f", "j", "k", "l", ";", "e", "i", "r", "u"]
            ),
            "difficulty_level": 6,
            "position": 6,
            "required_confidence": 1.0,
            "required_wpm": 35.0,
            "required_accuracy": 0.95,
        },
        # Lesson 7: Top row expansion
        {
            "name": "Top Row: W and O",
            "description": "Add more frequently used letters",
            "unlocked_keys": json.dumps(
                ["a", "s", "d", "f", "j", "k", "l", ";", "e", "i", "r", "u", "w", "o"]
            ),
            "difficulty_level": 7,
            "position": 7,
            "required_confidence": 1.0,
            "required_wpm": 35.0,
            "required_accuracy": 0.95,
        },
        # Lesson 8: More top row
        {
            "name": "Top Row: T and P",
            "description": "Expand vocabulary options",
            "unlocked_keys": json.dumps(
                ["a", "s", "d", "f", "j", "k", "l", ";", "e", "i", "r", "u", "w", "o", "t", "p"]
            ),
            "difficulty_level": 8,
            "position": 8,
            "required_confidence": 1.0,
            "required_wpm": 37.0,
            "required_accuracy": 0.95,
        },
        # Lesson 9: Complete top row letters
        {
            "name": "Top Row Complete",
            "description": "Master all top row letter keys",
            "unlocked_keys": json.dumps(
                [
                    "a",
                    "s",
                    "d",
                    "f",
                    "j",
                    "k",
                    "l",
                    ";",
                    "q",
                    "w",
                    "e",
                    "r",
                    "t",
                    "y",
                    "u",
                    "i",
                    "o",
                    "p",
                ]
            ),
            "difficulty_level": 9,
            "position": 9,
            "required_confidence": 1.0,
            "required_wpm": 40.0,
            "required_accuracy": 0.95,
        },
        # Lesson 10: Bottom row introduction
        {
            "name": "Bottom Row: V and M",
            "description": "Introduction to the bottom row",
            "unlocked_keys": json.dumps(
                [
                    "a",
                    "s",
                    "d",
                    "f",
                    "j",
                    "k",
                    "l",
                    ";",
                    "q",
                    "w",
                    "e",
                    "r",
                    "t",
                    "y",
                    "u",
                    "i",
                    "o",
                    "p",
                    "v",
                    "m",
                ]
            ),
            "difficulty_level": 10,
            "position": 10,
            "required_confidence": 1.0,
            "required_wpm": 40.0,
            "required_accuracy": 0.95,
        },
        # Lesson 11: More bottom row
        {
            "name": "Bottom Row: C and comma",
            "description": "Add more bottom row keys",
            "unlocked_keys": json.dumps(
                [
                    "a",
                    "s",
                    "d",
                    "f",
                    "j",
                    "k",
                    "l",
                    ";",
                    "q",
                    "w",
                    "e",
                    "r",
                    "t",
                    "y",
                    "u",
                    "i",
                    "o",
                    "p",
                    "v",
                    "m",
                    "c",
                    ",",
                ]
            ),
            "difficulty_level": 11,
            "position": 11,
            "required_confidence": 1.0,
            "required_wpm": 40.0,
            "required_accuracy": 0.95,
        },
        # Lesson 12: Complete bottom row
        {
            "name": "Bottom Row Complete",
            "description": "Master all bottom row keys",
            "unlocked_keys": json.dumps(
                [
                    "a",
                    "s",
                    "d",
                    "f",
                    "j",
                    "k",
                    "l",
                    ";",
                    "q",
                    "w",
                    "e",
                    "r",
                    "t",
                    "y",
                    "u",
                    "i",
                    "o",
                    "p",
                    "z",
                    "x",
                    "c",
                    "v",
                    "b",
                    "n",
                    "m",
                    ",",
                    ".",
                    "/",
                ]
            ),
            "difficulty_level": 12,
            "position": 12,
            "required_confidence": 1.0,
            "required_wpm": 45.0,
            "required_accuracy": 0.95,
        },
        # Lesson 13: All letters complete
        {
            "name": "All Letters",
            "description": "Practice all letter keys together",
            "unlocked_keys": json.dumps(
                [
                    "a",
                    "b",
                    "c",
                    "d",
                    "e",
                    "f",
                    "g",
                    "h",
                    "i",
                    "j",
                    "k",
                    "l",
                    "m",
                    "n",
                    "o",
                    "p",
                    "q",
                    "r",
                    "s",
                    "t",
                    "u",
                    "v",
                    "w",
                    "x",
                    "y",
                    "z",
                    ";",
                    ",",
                    ".",
                    "/",
                ]
            ),
            "difficulty_level": 13,
            "position": 13,
            "required_confidence": 1.0,
            "required_wpm": 45.0,
            "required_accuracy": 0.95,
        },
        # Lesson 14: Numbers introduction
        {
            "name": "Numbers: 1-5",
            "description": "Learn the left-hand number keys",
            "unlocked_keys": json.dumps(
                [
                    "a",
                    "b",
                    "c",
                    "d",
                    "e",
                    "f",
                    "g",
                    "h",
                    "i",
                    "j",
                    "k",
                    "l",
                    "m",
                    "n",
                    "o",
                    "p",
                    "q",
                    "r",
                    "s",
                    "t",
                    "u",
                    "v",
                    "w",
                    "x",
                    "y",
                    "z",
                    ";",
                    ",",
                    ".",
                    "/",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                ]
            ),
            "difficulty_level": 14,
            "position": 14,
            "required_confidence": 1.0,
            "required_wpm": 40.0,
            "required_accuracy": 0.93,
        },
        # Lesson 15: All numbers
        {
            "name": "Numbers Complete",
            "description": "Master all number keys",
            "unlocked_keys": json.dumps(
                [
                    "a",
                    "b",
                    "c",
                    "d",
                    "e",
                    "f",
                    "g",
                    "h",
                    "i",
                    "j",
                    "k",
                    "l",
                    "m",
                    "n",
                    "o",
                    "p",
                    "q",
                    "r",
                    "s",
                    "t",
                    "u",
                    "v",
                    "w",
                    "x",
                    "y",
                    "z",
                    ";",
                    ",",
                    ".",
                    "/",
                    "0",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                ]
            ),
            "difficulty_level": 15,
            "position": 15,
            "required_confidence": 1.0,
            "required_wpm": 40.0,
            "required_accuracy": 0.93,
        },
        # Lesson 16: Special characters
        {
            "name": "Special Characters",
            "description": "Learn common special characters",
            "unlocked_keys": json.dumps(
                [
                    "a",
                    "b",
                    "c",
                    "d",
                    "e",
                    "f",
                    "g",
                    "h",
                    "i",
                    "j",
                    "k",
                    "l",
                    "m",
                    "n",
                    "o",
                    "p",
                    "q",
                    "r",
                    "s",
                    "t",
                    "u",
                    "v",
                    "w",
                    "x",
                    "y",
                    "z",
                    ";",
                    ",",
                    ".",
                    "/",
                    "0",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "-",
                    "=",
                    "[",
                    "]",
                    "\\",
                    "'",
                    "`",
                ]
            ),
            "difficulty_level": 16,
            "position": 16,
            "required_confidence": 1.0,
            "required_wpm": 40.0,
            "required_accuracy": 0.90,
        },
    ]

    for lesson_data in lessons_data:
        lesson = Lesson(**lesson_data)
        db.add(lesson)

    db.commit()
    print(f"✓ Seeded {len(lessons_data)} lessons")
    db.close()


def seed_code_problems():
    """Seed code practice problems from JSON files."""
    from app.database import SessionLocal

    db = SessionLocal()

    # Check if problems already exist
    existing_count = db.query(CodeProblem).count()
    if existing_count > 0:
        print(f"✓ Code problems already seeded ({existing_count} problems found)")
        db.close()
        return

    print("Seeding code problems...")

    # Load problems from JSON files
    problems_dir = Path(settings.code_problems_dir)
    loaded = 0

    for language_dir in problems_dir.iterdir():
        if not language_dir.is_dir():
            continue

        for problem_file in language_dir.glob("*.json"):
            try:
                with open(problem_file) as f:
                    problem_data = json.load(f)

                problem = CodeProblem(
                    problem_id=problem_data["problem_id"],
                    title=problem_data["title"],
                    language=problem_data["language"],
                    difficulty=problem_data.get("difficulty"),
                    content=problem_data["content"],
                    category=problem_data.get("category"),
                )
                db.add(problem)
                loaded += 1
            except Exception as e:
                print(f"  Warning: Failed to load {problem_file}: {e}")

    db.commit()
    print(f"✓ Seeded {loaded} code problems")
    db.close()


def main():
    """Main initialization function."""
    print("=" * 50)
    print("Typing Assistant - Database Initialization")
    print("=" * 50)

    init_db()
    seed_lessons()
    seed_code_problems()

    print("\n" + "=" * 50)
    print("✓ Database initialization complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
