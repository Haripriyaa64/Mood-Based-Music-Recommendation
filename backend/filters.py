def build_filters(mood: str, context: dict) -> dict:
    activities = context.get("activities", ["general"])
    language = context.get("language", "english")

    # Base defaults
    filters = {
        "energy": 0.5,
        "valence": 0.5,
        "tempo": 100,
        "genre": language,
        "vibe": "chill",
        "query_terms": [],
    }

    # --- ACTIVITY (Primary signal) ---
    activity_map = {
        "gym":    {"energy": 0.92, "tempo": 135, "vibe": "high energy workout pump"},
        "party":  {"energy": 0.95, "tempo": 145, "vibe": "dance party banger"},
        "study":  {"energy": 0.25, "tempo": 75,  "vibe": "focus concentration"},
        "sleep":  {"energy": 0.08, "tempo": 55,  "vibe": "sleep calm soothing"},
        "travel": {"energy": 0.65, "tempo": 110, "vibe": "road trip feel good"},
        "relax":  {"energy": 0.2,  "tempo": 70,  "vibe": "relaxing peaceful"},
    }

    primary = activities[0]
    if primary in activity_map:
        filters.update(activity_map[primary])

    # Multi-activity blending
    if "gym" in activities and "party" in activities:
        filters["energy"] = 1.0
        filters["tempo"] = 148
        filters["vibe"] = "pump up party"

    # --- MOOD (Secondary signal) ---
    mood_adjustments = {
        "happy":    {"valence": +0.3, "energy": +0.1},
        "sad":      {"valence": -0.3, "energy": -0.1},
        "angry":    {"energy": +0.15},
        "stressed": {"energy": -0.15, "tempo": -15},
        "calm":     {"energy": -0.2, "valence": +0.1},
        "energetic":{"energy": +0.2, "tempo": +15},
        "neutral":  {},
    }

    adjustments = mood_adjustments.get(mood, {})
    for key, delta in adjustments.items():
        if key in filters:
            if key == "tempo":
                filters[key] = max(50, min(180, filters[key] + delta))
            else:
                filters[key] = max(0.0, min(1.0, filters[key] + delta))

    # Clamp values
    filters["energy"] = round(max(0.0, min(1.0, filters["energy"])), 2)
    filters["valence"] = round(max(0.0, min(1.0, filters["valence"])), 2)
    filters["tempo"] = int(max(50, min(180, filters["tempo"])))

    return filters