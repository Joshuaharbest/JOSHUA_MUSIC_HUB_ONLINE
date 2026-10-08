import os
from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

def youtube_search(q, limit=10):
    if not YOUTUBE_API_KEY:
        return {"items": [], "error": "YOUTUBE_API_KEY is not configured."}
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet", "q": q, "type": "video",
        "maxResults": min(limit, 25), "key": YOUTUBE_API_KEY
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    items = []
    for x in data.get("items", []):
        vid = x.get("id", {}).get("videoId")
        if not vid:
            continue
        s = x.get("snippet", {})
        items.append({
            "title": s.get("title", ""),
            "channel": s.get("channelTitle", ""),
            "thumbnail": s.get("thumbnails", {}).get("medium", {}).get("url", ""),
            "url": f"https://www.youtube.com/watch?v={vid}",
            "source": "YouTube"
        })
    return {"items": items}

def spotify_token():
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return None
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
        timeout=15
    )
    r.raise_for_status()
    return r.json()["access_token"]

def spotify_search(q, limit=10):
    token = spotify_token()
    if not token:
        return {"items": [], "error": "Spotify API credentials are not configured."}
    r = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {token}"},
        params={"q": q, "type": "track", "limit": min(limit, 50)},
        timeout=15
    )
    r.raise_for_status()
    data = r.json()
    items = []
    for t in data.get("tracks", {}).get("items", []):
        artists = ", ".join(a["name"] for a in t.get("artists", []))
        images = t.get("album", {}).get("images", [])
        items.append({
            "title": t.get("name", ""),
            "channel": artists,
            "thumbnail": images[1]["url"] if len(images) > 1 else (images[0]["url"] if images else ""),
            "url": t.get("external_urls", {}).get("spotify", ""),
            "source": "Spotify"
        })
    return {"items": items}

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/api/search")
def search():
    q = request.args.get("q", "").strip()
    source = request.args.get("source", "all")
    if not q:
        return jsonify({"items": [], "errors": []})
    items, errors = [], []
    try:
        if source in ("all", "youtube"):
            result = youtube_search(q)
            items.extend(result["items"])
            if result.get("error"): errors.append(result["error"])
    except Exception as e:
        errors.append(f"YouTube: {e}")
    try:
        if source in ("all", "spotify"):
            result = spotify_search(q)
            items.extend(result["items"])
            if result.get("error"): errors.append(result["error"])
    except Exception as e:
        errors.append(f"Spotify: {e}")
    return jsonify({"items": items, "errors": errors})

@app.get("/health")
def health():
    return jsonify({"status": "ok", "youtube": bool(YOUTUBE_API_KEY),
                    "spotify": bool(SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
