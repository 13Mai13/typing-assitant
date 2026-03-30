"""Adaptive lesson progression service.

Implements keybr-style adaptive difficulty based on per-key confidence scoring.
Keys are unlocked progressively as the user demonstrates mastery.
"""

from typing import NamedTuple


class KeyStats(NamedTuple):
    """Statistics for a single key."""

    key_char: str
    total_presses: int
    correct_presses: int
    avg_press_time: float  # in milliseconds
    confidence_score: float


# Key introduction order based on frequency and ergonomics
KEY_INTRODUCTION_ORDER = [
    # Home row (start here for touch typing foundation)
    "f",
    "j",
    "d",
    "k",
    "s",
    "l",
    "a",
    ";",
    # Top row (most common letters first)
    "e",
    "i",
    "r",
    "u",
    "w",
    "o",
    "t",
    "p",
    "q",
    "y",
    # Bottom row
    "v",
    "m",
    "c",
    ",",
    "x",
    ".",
    "z",
    "/",
    # Numbers (later stage)
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]


def calculate_key_confidence(
    total_presses: int,
    correct_presses: int,
    avg_press_time: float,
) -> float:
    """Calculate confidence score for a key (0.0 to 1.0).

    Confidence is based on both accuracy and speed. The algorithm:
    1. Accuracy score: correct_presses / total_presses
    2. Speed score: penalizes slow typing (target: 175ms = 35 WPM)
    3. Attempt factor: requires minimum attempts before full confidence
    4. Final: weighted combination (60% accuracy, 40% speed)

    Args:
        total_presses: Total number of times key was pressed
        correct_presses: Number of correct presses
        avg_press_time: Average time to press key in milliseconds

    Returns:
        Confidence score from 0.0 to 1.0

    Example:
        >>> # Perfect accuracy, fast typing, enough attempts
        >>> calculate_key_confidence(50, 50, 150.0)
        1.0
        >>> # Perfect accuracy but slow
        >>> round(calculate_key_confidence(50, 50, 350.0), 2)
        0.6
        >>> # Not enough attempts yet
        >>> round(calculate_key_confidence(10, 10, 150.0), 2)
        0.2
    """
    if total_presses == 0:
        return 0.0

    # Accuracy component (0.0 to 1.0)
    accuracy = correct_presses / total_presses

    # Speed component (0.0 to 1.0)
    # Target: 35 WPM ≈ 175ms per character (5 chars/word, 60000ms/min)
    target_time_ms = 175.0

    if avg_press_time <= target_time_ms:
        speed_score = 1.0
    else:
        # Penalize slower typing exponentially
        slowness_factor = (avg_press_time - target_time_ms) / target_time_ms
        speed_score = max(0.0, 1.0 - slowness_factor)

    # Attempt factor: require minimum 50 attempts before full confidence
    # This prevents lucky streaks from unlocking keys too early
    min_attempts = 50
    attempt_factor = min(1.0, total_presses / min_attempts)

    # Weighted combination: accuracy is more important than speed
    confidence = (accuracy * 0.6 + speed_score * 0.4) * attempt_factor

    return round(confidence, 3)


def should_unlock_next_key(current_keys_stats: list[KeyStats]) -> tuple[bool, str | None]:
    """Determine if user is ready for a new key to be introduced.

    Args:
        current_keys_stats: List of KeyStats for currently unlocked keys

    Returns:
        Tuple of (should_unlock, next_key_char)
        - should_unlock: True if ready for new key
        - next_key_char: The next key to introduce, or None if not ready

    Example:
        >>> stats = [
        ...     KeyStats('f', 50, 50, 150.0, 1.0),
        ...     KeyStats('j', 50, 50, 150.0, 1.0),
        ... ]
        >>> should_unlock_next_key(stats)
        (True, 'd')
        >>> weak_stats = [
        ...     KeyStats('f', 50, 50, 150.0, 1.0),
        ...     KeyStats('j', 20, 15, 300.0, 0.5),
        ... ]
        >>> should_unlock_next_key(weak_stats)
        (False, None)
    """
    # Check if all current keys have high confidence
    if not current_keys_stats:
        # No keys yet, start with first two
        return True, KEY_INTRODUCTION_ORDER[0]

    # All keys must have confidence >= 1.0 to unlock next key
    all_keys_confident = all(key_stat.confidence_score >= 1.0 for key_stat in current_keys_stats)

    if not all_keys_confident:
        return False, None

    # Find next key to introduce
    current_keys = {key_stat.key_char for key_stat in current_keys_stats}

    for key_char in KEY_INTRODUCTION_ORDER:
        if key_char not in current_keys:
            return True, key_char

    # All keys already unlocked
    return False, None


def get_next_lesson_keys(current_lesson_keys: list[str]) -> list[str] | None:
    """Get the next set of keys for progressive lesson advancement.

    Args:
        current_lesson_keys: List of keys in the current lesson

    Returns:
        List of keys for the next lesson, or None if no more keys to add

    Example:
        >>> get_next_lesson_keys(['f', 'j'])
        ['f', 'j', 'd']
    """
    current_set = set(current_lesson_keys)

    # Find the next key in the introduction order
    for key_char in KEY_INTRODUCTION_ORDER:
        if key_char not in current_set:
            # Return current keys plus the new one
            return current_lesson_keys + [key_char]

    # All keys already included
    return None
