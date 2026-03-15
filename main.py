from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube API Running"

@app.route("/play")
def play():

    query = request.args.get("q")

    ydl_opts = {
        "quiet": True,
        "format": "best",
        "default_search": "ytsearch",
        "noplaylist": True,
        "cookiefile": "cookies.txt"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)

        video = info["entries"][0]
        vid = video["id"]

        stream = video.get("url")

        if not stream and "formats" in video:
            stream = video["formats"][-1]["url"]

        return jsonify({
            "title": video["title"],
            "duration": video.get("duration"),
            "thumbnail": f"https://img.youtube.com/vi/{vid}/hqdefault.jpg",
            "stream": stream
        })

    except Exception as e:
        return jsonify({"error": str(e)})

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
