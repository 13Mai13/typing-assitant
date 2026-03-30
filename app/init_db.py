"""Database initialization script.

Run this script to create all tables and seed initial data:
    python -m app.init_db
"""

import json

from app.config import settings
from app.database import Base, engine
from app.models import Lesson


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
    ]

    for lesson_data in lessons_data:
        lesson = Lesson(**lesson_data)
        db.add(lesson)

    db.commit()
    print(f"✓ Seeded {len(lessons_data)} lessons")
    db.close()


def main():
    """Main initialization function."""
    print("=" * 50)
    print("Typing Assistant - Database Initialization")
    print("=" * 50)

    init_db()
    seed_lessons()

    print("\n" + "=" * 50)
    print("✓ Database initialization complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
