from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Music API Running"

@app.route("/search")
def search():

    query = request.args.get("q")

    if not query:
        return jsonify({"error": "No query provided"})

    ydl_opts = {
        "quiet": True,
        "format": "best",
        "default_search": "ytsearch",
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)

        video = info["entries"][0]

        data = {
            "title": video.get("title"),
            "duration": video.get("duration"),
            "thumbnail": video.get("thumbnail"),
            "video_url": f"https://youtube.com/watch?v={video['id']}",
            "stream": video.get("url")   # 🔥 direct stream
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
