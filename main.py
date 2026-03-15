from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/search")
def search():

    query = request.args.get("q")

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
        video = info["entries"][0]

    data = {
        "title": video["title"],
        "duration": video["duration"],
        "thumbnail": video["thumbnail"],
        "video_url": f"https://youtube.com/watch?v={video['id']}"
    }

    return jsonify(data)

@app.route("/stream")
def stream():

    url = request.args.get("url")

    ydl_opts = {
        "format": "best"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return jsonify({
        "stream": info["url"]
    })

app.run(host="0.0.0.0", port=5000)
