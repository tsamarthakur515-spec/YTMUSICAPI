from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Music API Running"

# SEARCH API
@app.route("/search")
def search():

    query = request.args.get("q")

    if not query:
        return jsonify({"error": "No query provided"})

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "default_search": "ytsearch"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)

        video = info["entries"][0]
        video_id = video["id"]

        data = {
            "title": video.get("title"),
            "duration": video.get("duration"),
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
            "video_url": f"https://youtube.com/watch?v={video_id}"
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

# STREAM API
@app.route("/stream")
def stream():

    url = request.args.get("url")

    if not url:
        return jsonify({"error": "No URL provided"})

    ydl_opts = {
        "quiet": True,
        "format": "best[ext=mp4]/best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        stream_url = info.get("url")

        # fallback if url not found
        if not stream_url and "formats" in info:
            stream_url = info["formats"][-1]["url"]

        return jsonify({
            "stream": stream_url
        })

    except Exception as e:
        return jsonify({"error": str(e)})

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
