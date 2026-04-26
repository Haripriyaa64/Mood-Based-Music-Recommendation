from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

from nlp import detect_mood
from context import extract_context
from filters import build_filters
from youtube import get_songs, build_query

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🎧 Smart Music Recommender API is running", "status": "ok"})


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json(force=True)

        if not data or "input" not in data:
            return jsonify({"error": "No input provided"}), 400

        user_input = data["input"].strip()
        if not user_input:
            return jsonify({"error": "Empty input"}), 400

        # Pipeline
        mood    = detect_mood(user_input)
        context = extract_context(user_input)
        filters = build_filters(mood, context)

        # Pass activity info into filters so youtube.py can use it
        filters["_activities"] = context.get("activities", ["general"])

        songs   = get_songs(filters)

        # Clean private keys before returning
        clean_filters = {k: v for k, v in filters.items() if not k.startswith("_")}

        return jsonify({
            "input":   user_input,
            "mood":    mood,
            "context": context,
            "filters": clean_filters,
            "query":   build_query(filters),
            "songs":   songs,
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500


@app.route("/debug", methods=["POST"])
def debug():
    data = request.get_json(force=True)
    user_input = data.get("input", "")
    mood    = detect_mood(user_input)
    context = extract_context(user_input)
    filters = build_filters(mood, context)
    return jsonify({"input": user_input, "mood": mood, "context": context, "filters": filters})


if __name__ == "__main__":
    app.run(debug=True, port=5000)