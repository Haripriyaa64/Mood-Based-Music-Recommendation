import re

ACTIVITY_KEYWORDS = {
    "gym":    ["gym", "workout", "exercise", "fitness", "training", "lifting", "weights", "running", "beast mode"],
    "study":  ["study", "studying", "focus", "reading", "exam", "coding", "work", "concentrate", "productive"],
    "sleep":  ["sleep", "sleeping", "night", "bed", "bedtime", "rest", "resting", "nap"],
    "travel": ["travel", "trip", "drive", "driving", "journey", "road", "commute", "bus", "flight"],
    "party":  ["party", "dance", "dancing", "club", "celebration", "celebrate", "night out", "dj"],
    "relax":  ["relax", "relaxing", "chill", "chilling", "lounge", "meditation", "meditate", "unwind"],
}

LANGUAGE_KEYWORDS = {
    "punjabi": ["punjabi", "panjabi"],
    "hindi":   ["hindi", "bollywood", "desi"],
    "tamil":   ["tamil", "kollywood"],
    "telugu":  ["telugu", "tollywood"],
    "english": ["english", "western", "pop"],
    "lofi":    ["lofi", "lo-fi", "lo fi", "chill beats"],
    "edm":     ["edm", "dj", "electronic", "techno", "house"],
    "rap":     ["rap", "hip hop", "hiphop", "hip-hop"],
    "classical": ["classical", "instrumental", "orchestral"],
}


def clean_text(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text.lower())


def extract_context(text: str) -> dict:
    cleaned = clean_text(text)

    activities = []
    for key, words in ACTIVITY_KEYWORDS.items():
        if any(w in cleaned for w in words):
            activities.append(key)

    languages = []
    for key, words in LANGUAGE_KEYWORDS.items():
        if any(w in cleaned for w in words):
            languages.append(key)

    return {
        "activities": activities or ["general"],
        "language": languages[0] if languages else "english",
        "all_languages": languages,
    }