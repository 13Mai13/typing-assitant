"""Lesson text generation service.

Generates practice text using pseudo-words with emphasis on weak keys.
Inspired by keybr.com's approach to adaptive practice.
"""

import random


def generate_pseudo_word(
    available_keys: list[str], min_length: int = 3, max_length: int = 7
) -> str:
    """Generate a pronounceable pseudo-word using available keys.

    Creates words following consonant-vowel patterns when possible,
    making them easier to type and remember.

    Args:
        available_keys: List of available character keys
        min_length: Minimum word length (default: 3)
        max_length: Maximum word length (default: 7)

    Returns:
        A randomly generated pseudo-word

    Example:
        >>> random.seed(42)
        >>> generate_pseudo_word(['f', 'j', 'a', 'e'])
        'jafe'
    """
    vowels = [k for k in available_keys if k in "aeiou"]
    consonants = [k for k in available_keys if k not in "aeiou" and k.isalpha()]

    # If we don't have both vowels and consonants yet, use random combinations
    if not vowels or not consonants:
        length = random.randint(min_length, max_length)
        # Filter to only alphabetic characters
        alpha_keys = [k for k in available_keys if k.isalpha()]
        if not alpha_keys:
            # Fallback to all available keys
            alpha_keys = available_keys
        return "".join(random.choices(alpha_keys, k=length))

    # Build word with consonant-vowel pattern for pronounceability
    word = []
    length = random.randint(min_length, max_length)

    for i in range(length):
        if i % 2 == 0:
            # Consonant on even positions
            word.append(random.choice(consonants))
        else:
            # Vowel on odd positions
            word.append(random.choice(vowels))

    return "".join(word)


def generate_practice_text(
    available_keys: list[str],
    word_count: int = 50,
    weak_keys: list[str] | None = None,
) -> str:
    """Generate practice text with emphasis on weak keys.

    Creates a string of pseudo-words for typing practice. If weak keys
    are provided, 30% of words will heavily feature those keys to provide
    targeted practice.

    Args:
        available_keys: List of keys available for this lesson
        word_count: Number of words to generate (default: 50)
        weak_keys: Optional list of keys that need extra practice

    Returns:
        Space-separated string of pseudo-words

    Example:
        >>> random.seed(42)
        >>> text = generate_practice_text(['f', 'j', 'd', 'k'], word_count=5)
        >>> len(text.split())
        5
    """
    words = []

    if weak_keys and len(weak_keys) > 0:
        # 30% of words should heavily feature weak keys
        weak_word_count = int(word_count * 0.3)

        # Generate words emphasizing weak keys
        for _ in range(weak_word_count):
            # Boost weak key frequency by including them multiple times
            biased_keys = available_keys + weak_keys * 3
            words.append(generate_pseudo_word(biased_keys))

        # Generate remaining words with normal distribution
        for _ in range(word_count - weak_word_count):
            words.append(generate_pseudo_word(available_keys))
    else:
        # No weak keys specified, generate all words normally
        for _ in range(word_count):
            words.append(generate_pseudo_word(available_keys))

    return " ".join(words)


def identify_weak_keys(
    key_statistics: list[tuple[str, float]], confidence_threshold: float = 0.8
) -> list[str]:
    """Identify keys that need extra practice based on confidence scores.

    Args:
        key_statistics: List of tuples (key_char, confidence_score)
        confidence_threshold: Keys below this score are considered weak (default: 0.8)

    Returns:
        List of key characters that need more practice

    Example:
        >>> identify_weak_keys([('f', 1.0), ('j', 0.7), ('d', 0.9), ('k', 0.6)])
        ['j', 'k']
    """
    weak_keys = []
    for key_char, confidence in key_statistics:
        if confidence < confidence_threshold:
            weak_keys.append(key_char)

    return weak_keys
