import urllib.parse
import urllib.request
import json
import re
import random


# ── Curated real YouTube video IDs per query type ──────────────────────────────
# These are actual popular videos — fallback when scraping fails.
CURATED = {
    "gym_punjabi": [
        ("Tere Te – AP Dhillon", "AP Dhillon", "dBtDFHblxpA"),
        ("Brown Munde – AP Dhillon", "AP Dhillon", "UZPFCqNfMvE"),
        ("GOAT – Diljit Dosanjh", "Diljit Dosanjh", "nKJJPMYPPBQ"),
        ("G.O.A.T – Diljit Dosanjh (Full Album)", "Diljit Dosanjh", "nKJJPMYPPBQ"),
        ("Lover – Diljit Dosanjh", "Diljit Dosanjh", "yE8cYOmNsxg"),
        ("Imma Balla – Sidhu Moosewala", "Sidhu Moosewala", "1K-W5NTUA8Q"),
        ("295 – Sidhu Moosewala", "Sidhu Moosewala", "nfSCd5s2628"),
        ("HAAN – Karan Aujla", "Karan Aujla", "9jh2tpF3Vjk"),
        ("52 Bars – Karan Aujla", "Karan Aujla", "FKbw0TXxasw"),
        ("Kinni Kinni – Diljit Dosanjh", "Diljit Dosanjh", "cxBpHCr2TsE"),
    ],
    "gym_hindi": [
        ("Zinda – Bhaag Milkha Bhaag", "Amit Trivedi", "W7-KTMhAo2g"),
        ("Kar Har Maidaan Fateh – Sanju", "Sukhwinder Singh", "MiRCCYzJXqs"),
        ("Sultan Title Track", "Sukhwinder Singh", "Z14dcLiVhJk"),
        ("Jaa Re – Race 3", "Vishal-Shekhar", "Ug0fJg5-jvs"),
        ("Bhaari Pao – Bhaukaal", "Various", "3R59XCBR44A"),
    ],
    "gym_english": [
        ("Eye of the Tiger – Survivor", "Survivor", "btPJPFnesV4"),
        ("Till I Collapse – Eminem", "Eminem", "ytQ5ob8bQEA"),
        ("Lose Yourself – Eminem", "Eminem", "_Yhyp-_hX2s"),
        ("Can't Hold Us – Macklemore", "Macklemore", "2zNSgSzhBfM"),
        ("Stronger – Kanye West", "Kanye West", "PsO6ZnUZI0g"),
        ("Work Hard Play Hard – Wiz Khalifa", "Wiz Khalifa", "oVfBFzNQr2A"),
    ],
    "party_punjabi": [
        ("Illegal Weapon 2.0", "Garry Sandhu", "yiWgkxQEMMs"),
        ("Muchh – Jass Manak", "Jass Manak", "8wGqTGniWMY"),
        ("Viah – Jass Manak", "Jass Manak", "YhRCCT6EB6U"),
        ("Coka – Sukhe", "Sukhe", "YiGOjG_NRZE"),
        ("Naah – Harrdy Sandhu", "Harrdy Sandhu", "p4oohBkNnNA"),
    ],
    "party_hindi": [
        ("Badtameez Dil – YJHD", "Pritam", "II2EO3opT1E"),
        ("Desi Beat – RA.One", "Vishal-Shekhar", "GjYHWwjlNe8"),
        ("Lungi Dance", "Yo Yo Honey Singh", "Ofm-Ro5TNc0"),
        ("Tamma Tamma Again – Badrinath Ki Dulhania", "Akhil Sachdeva", "yWX0XKGV0Bg"),
        ("Kala Chashma – Baar Baar Dekho", "Badshah", "k4yXQeaUmtE"),
    ],
    "party_english": [
        ("Blinding Lights – The Weeknd", "The Weeknd", "4NRXx6U8ABQ"),
        ("Levitating – Dua Lipa", "Dua Lipa", "TUVcZfQe-Kw"),
        ("Save Your Tears – The Weeknd", "The Weeknd", "XXYlFuWEuKI"),
        ("As It Was – Harry Styles", "Harry Styles", "H5v3kku4y6Q"),
        ("Anti-Hero – Taylor Swift", "Taylor Swift", "b1kbLwvqugk"),
    ],
    "study_lofi": [
        ("Lofi Hip Hop – Study Beats", "ChilledCow", "jfKfPfyJRdk"),
        ("Study With Me – 4 Hours Lofi", "Lofi Girl", "5qap5aO4i9A"),
        ("Jazz & Lofi – Study Session", "College Music", "lP9bCd_NSmE"),
        ("Lofi Chill Beats – 1 Hour", "Ambition", "iAMuvMDe8Eo"),
        ("Coffee Shop Ambience + Lofi", "Jason Lewis", "h2zkV1zym7Y"),
    ],
    "study_english": [
        ("The Best Study Music – Piano", "Study Music", "WPni755-Krg"),
        ("Mozart for the Brain – Focus", "Various", "e5bPSKaODio"),
        ("Brain Power – Study Music", "Greenred Productions", "5OwuNHGFBos"),
        ("Classical Music for Studying", "Various", "AAABDSvJnxQ"),
    ],
    "sleep_calm": [
        ("Relaxing Sleep Music – Deep Sleeping", "Yellow Brick Cinema", "1ZYbU82GVz4"),
        ("8 Hour Sleep Music – Delta Waves", "PowerThoughts", "9vnxkCBJjqQ"),
        ("Peaceful Night – Sleep Sounds", "Soothing Relaxation", "9MKdJjU-pIY"),
        ("Rain Sounds for Sleeping", "Nature Sounds", "q76bMs-NwRk"),
    ],
    "travel_english": [
        ("Life is a Highway – Rascal Flatts", "Rascal Flatts", "Ay8CGVN8gR4"),
        ("On the Road Again – Willie Nelson", "Willie Nelson", "9RM5u3EbWkY"),
        ("Highway to Hell – AC/DC", "AC/DC", "l482T0yNkeo"),
        ("Bohemian Rhapsody – Queen", "Queen", "fJ9rUzIMcZQ"),
        ("Africa – Toto", "Toto", "FTQbiNvZqaY"),
    ],
    "relax_english": [
        ("Weightless – Marconi Union", "Marconi Union", "UfcAVejslrU"),
        ("Clair de Lune – Debussy", "Claude Debussy", "WNcsUNKnbDY"),
        ("Chill Acoustic Guitar", "Acoustic Hits", "2gkDYgj2VLM"),
        ("Peaceful Piano – 1 Hour", "Peder B. Helland", "77ZozI0rw7w"),
    ],
    "relax_hindi": [
        ("Tum Hi Ho – Aashiqui 2", "Arijit Singh", "Umqb9KENgmk"),
        ("Channa Mereya – ADHM", "Arijit Singh", "zaHxwnqKVUE"),
        ("Kabira – Yeh Jawaani Hai Deewani", "Rekha Bhardwaj", "NJZck_b-OsY"),
        ("Kal Ho Naa Ho Title", "Sonu Nigam", "RWHpGbsWaF8"),
    ],
    "default": [
        ("Shape of You – Ed Sheeran", "Ed Sheeran", "JGwWNGJdvx8"),
        ("Blinding Lights – The Weeknd", "The Weeknd", "4NRXx6U8ABQ"),
        ("Levitating – Dua Lipa", "Dua Lipa", "TUVcZfQe-Kw"),
        ("Stay – The Kid LAROI", "The Kid LAROI", "kTJczUoc26U"),
        ("Drivers License – Olivia Rodrigo", "Olivia Rodrigo", "ZmDBbnmKpqQ"),
    ],
}


def _pick_curated(filters: dict) -> list:
    """Pick the best curated list based on activity + language."""
    activities = filters.get("_activities", ["general"])
    language = filters.get("genre", "english")

    primary = activities[0] if activities else "general"

    # Build candidate keys in priority order
    candidates = [
        f"{primary}_{language}",
        f"{primary}_english",
        f"default_{language}",
        "default",
    ]

    for key in candidates:
        if key in CURATED:
            pool = CURATED[key]
            selected = random.sample(pool, min(6, len(pool)))
            return [
                {
                    "name": title,
                    "artist": artist,
                    "url": f"https://www.youtube.com/watch?v={vid_id}",
                    "image": f"https://img.youtube.com/vi/{vid_id}/mqdefault.jpg",
                    "video_id": vid_id,
                }
                for title, artist, vid_id in selected
            ]

    return []


def _try_scrape_youtube(query: str, max_results: int = 6) -> list:
    """
    Attempt to scrape YouTube search results page for real video IDs.
    Returns list of song dicts or empty list on failure.
    """
    try:
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"

        req = urllib.request.Request(url, headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        })

        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # Extract ytInitialData JSON
        match = re.search(r"var ytInitialData\s*=\s*(\{.*?\});\s*</script>", html, re.DOTALL)
        if not match:
            return []

        data = json.loads(match.group(1))

        # Navigate to video renderers
        contents = (
            data.get("contents", {})
            .get("twoColumnSearchResultsRenderer", {})
            .get("primaryContents", {})
            .get("sectionListRenderer", {})
            .get("contents", [])
        )

        songs = []
        for section in contents:
            items = section.get("itemSectionRenderer", {}).get("contents", [])
            for item in items:
                vr = item.get("videoRenderer")
                if not vr:
                    continue

                vid_id = vr.get("videoId", "")
                title = (
                    vr.get("title", {})
                    .get("runs", [{}])[0]
                    .get("text", "Unknown Title")
                )
                artist = (
                    vr.get("longBylineText", {})
                    .get("runs", [{}])[0]
                    .get("text", "Unknown Artist")
                )

                if vid_id:
                    songs.append({
                        "name": title,
                        "artist": artist,
                        "url": f"https://www.youtube.com/watch?v={vid_id}",
                        "image": f"https://img.youtube.com/vi/{vid_id}/mqdefault.jpg",
                        "video_id": vid_id,
                    })

                if len(songs) >= max_results:
                    break

            if len(songs) >= max_results:
                break

        return songs

    except Exception as e:
        print(f"[youtube] scrape failed: {e}")
        return []


def build_query(filters: dict) -> str:
    """Build a meaningful YouTube search query."""
    genre = filters.get("genre", "english")
    vibe = filters.get("vibe", "")
    energy = filters.get("energy", 0.5)

    # Convert genre to readable label
    genre_label = {
        "punjabi": "Punjabi",
        "hindi": "Hindi",
        "tamil": "Tamil",
        "telugu": "Telugu",
        "english": "",
        "lofi": "Lofi",
        "edm": "EDM",
        "rap": "Hip Hop",
        "classical": "Classical",
    }.get(genre, genre.title())

    # Activity-specific refined queries
    activities = filters.get("_activities", ["general"])
    primary = activities[0] if activities else "general"

    templates = {
        "gym":    f"{genre_label} {vibe} songs 2024",
        "party":  f"{genre_label} {vibe} hits 2024",
        "study":  f"{genre_label} {vibe} music for studying",
        "sleep":  f"{vibe} music for deep sleep",
        "travel": f"{genre_label} {vibe} road trip songs",
        "relax":  f"{genre_label} {vibe} relaxing songs",
        "general": f"{genre_label} {vibe} songs 2024",
    }

    query = templates.get(primary, f"{genre_label} {vibe} songs")
    return " ".join(query.split())  # clean extra spaces


def get_songs(filters: dict) -> list:
    """Return song recommendations — tries live scrape, falls back to curated."""
    query = build_query(filters)
    print(f"[youtube] search query: '{query}'")

    # Try live scrape first
    results = _try_scrape_youtube(query, max_results=6)

    if len(results) >= 4:
        print(f"[youtube] got {len(results)} live results")
        return results

    # Fallback to curated list
    print("[youtube] using curated fallback")
    return _pick_curated(filters)