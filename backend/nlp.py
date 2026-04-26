from textblob import TextBlob

# Emotion keywords — order matters (more specific first)
EMOTION_KEYWORDS = {
    "angry":   ["angry", "mad", "furious", "rage", "pissed", "frustrated", "annoyed", "irritated"],
    "stressed":["stress", "stressed", "pressure", "overwhelmed", "anxious", "anxiety", "tensed", "nervous"],
    "sad":     ["sad", "depressed", "down", "cry", "crying", "bad day", "upset", "lonely", "heartbreak", "heartbroken", "miss", "gloomy"],
    "happy":   ["happy", "excited", "great", "awesome", "good", "fun", "joy", "joyful", "cheerful", "celebrate", "love", "wonderful"],
    "calm":    ["relax", "relaxing", "peace", "peaceful", "calm", "chill", "soothe", "soothing", "unwind", "meditate"],
    "energetic": ["hype", "hyped", "pump", "pumped", "beast mode", "motivated", "energy", "fire", "lit"],
}


def keyword_emotion(text: str):
    text = text.lower()
    for emotion, words in EMOTION_KEYWORDS.items():
        for word in words:
            if word in text:
                return emotion
    return None


def detect_mood(text: str) -> str:
    emotion = keyword_emotion(text)
    if emotion:
        return emotion

    # TextBlob sentiment fallback
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    return "neutral"