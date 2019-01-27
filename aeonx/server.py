from flask import Flask, request, jsonify
from threading import Thread
from .Data import Data

app = Flask(__name__)

data = Data()


@app.route("/")
def root():
    return "aeon: saving your online time since 2019"


@app.route("/heatmap", methods=['POST'])
def update_heatmap():
    params = request.form
    new_data = params['data']
    video_id = params['videoId']
    result = data.update_heatmap(video_id, new_data)
    return result


@app.route("/video/<video_id>", methods=['GET','POST'])
def get_video(video_id):
    video = data.find_video(video_id)
    if video is not None:
        return jsonify(video)
    else:
        fetch_thread = Thread(target=data.add_video, kwargs={'video_id': video_id})
        fetch_thread.start()
        return "Video not found, getting"


app.run(debug=True)
