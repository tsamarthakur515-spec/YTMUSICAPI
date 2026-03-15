from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube Music API Running"

@app.route("/play")
def play():

    query = request.args.get("q")

    if not query:
        return jsonify({"error": "No query provided"})

    ydl_opts = {
        "quiet": True,
        "format": "best[ext=mp4]/best",
        "noplaylist": True,
        "default_search": "ytsearch",
        "extract_flat": False,
        "nocheckcertificate": True
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)

        video = info["entries"][0]

        video_id = video["id"]

        stream = video.get("url")

        if not stream and "formats" in video:
            stream = video["formats"][-1]["url"]

        data = {
            "title": video.get("title"),
            "duration": video.get("duration"),
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
            "stream": stream
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
