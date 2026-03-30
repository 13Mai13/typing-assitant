"""WPM (Words Per Minute) and accuracy calculation service.

Implements standard typing test metrics calculation following
industry conventions: 5 characters = 1 word.
"""


def calculate_metrics(session_data: dict) -> dict:
    """Calculate typing metrics from session data.

    Args:
        session_data: Dictionary containing:
            - total_keystrokes: Total number of keys pressed
            - correct_keystrokes: Number of correct keys
            - incorrect_keystrokes: Number of incorrect keys
            - duration_seconds: Session duration in seconds

    Returns:
        Dictionary with:
            - gross_wpm: Gross words per minute (no error penalty)
            - net_wpm: Net words per minute (adjusted for accuracy)
            - accuracy: Accuracy percentage (0-100)

    Example:
        >>> calculate_metrics({
        ...     'total_keystrokes': 250,
        ...     'correct_keystrokes': 250,
        ...     'incorrect_keystrokes': 0,
        ...     'duration_seconds': 60
        ... })
        {'gross_wpm': 50.0, 'net_wpm': 50.0, 'accuracy': 100.0}
    """
    # Handle edge case of no keystrokes or no duration
    if session_data["total_keystrokes"] == 0:
        return {"gross_wpm": 0.0, "net_wpm": 0.0, "accuracy": 0.0}

    if session_data["duration_seconds"] <= 0:
        return {"gross_wpm": 0.0, "net_wpm": 0.0, "accuracy": 0.0}

    # Convert duration to minutes
    duration_minutes = session_data["duration_seconds"] / 60.0

    # Standard: 5 characters = 1 word
    total_words = session_data["total_keystrokes"] / 5.0

    # Gross WPM: total speed without error penalty
    gross_wpm = total_words / duration_minutes

    # Calculate accuracy
    accuracy = session_data["correct_keystrokes"] / session_data["total_keystrokes"]

    # Net WPM: gross WPM adjusted for accuracy (modern approach)
    # This is more forgiving than subtracting (errors / time)
    net_wpm = max(0, gross_wpm * accuracy)

    return {
        "gross_wpm": round(gross_wpm, 2),
        "net_wpm": round(net_wpm, 2),
        "accuracy": round(accuracy * 100, 2),  # Convert to percentage
    }


def calculate_real_time_wpm(keystrokes_so_far: int, elapsed_seconds: float) -> float:
    """Calculate current WPM for real-time display during typing.

    Args:
        keystrokes_so_far: Number of keys pressed so far
        elapsed_seconds: Time elapsed in seconds

    Returns:
        Current WPM rounded to 1 decimal place

    Example:
        >>> calculate_real_time_wpm(100, 30)
        40.0
    """
    if elapsed_seconds < 1:
        return 0.0

    words = keystrokes_so_far / 5.0
    minutes = elapsed_seconds / 60.0
    wpm = words / minutes

    return round(wpm, 1)


def calculate_real_time_accuracy(correct_keystrokes: int, total_keystrokes: int) -> float:
    """Calculate current accuracy for real-time display.

    Args:
        correct_keystrokes: Number of correct keys pressed
        total_keystrokes: Total number of keys pressed

    Returns:
        Accuracy percentage rounded to 1 decimal place

    Example:
        >>> calculate_real_time_accuracy(95, 100)
        95.0
    """
    if total_keystrokes == 0:
        return 100.0

    accuracy = (correct_keystrokes / total_keystrokes) * 100
    return round(accuracy, 1)
