# JOSHUA MUSIC HUB ONLINE

Python/Flask web version of the desktop Media Downloader concept.

## Features
- Browser-based dark UI
- YouTube search
- Spotify track search
- Open results directly on the official platform
- Responsive desktop/mobile layout
- Render-ready with Gunicorn
- API keys stay on the server as environment variables

## 1. Install locally

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure the variables. Then run:

```bash
python app.py
```

Open http://127.0.0.1:5000

## 2. YouTube API

Create a YouTube Data API v3 key in Google Cloud and set:

`YOUTUBE_API_KEY`

## 3. Spotify API

Create an app in the Spotify Developer Dashboard and set:

`SPOTIFY_CLIENT_ID`
`SPOTIFY_CLIENT_SECRET`

This version uses Spotify Client Credentials for public catalog search. User-specific Spotify login/playlists require OAuth and can be added as the next module.

## 4. Render

- Create a GitHub repository named `joshua-music-hub`
- Upload these files
- Render -> New + -> Web Service
- Runtime: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Add the three environment variables in Render Environment
- Deploy

## Important

Do not put API keys directly in Python or JavaScript. Do not commit `.env`.

The web app opens YouTube/Spotify results on their official services. Any downloading feature should only be used for content you are authorized to download and should comply with the applicable platform terms.
