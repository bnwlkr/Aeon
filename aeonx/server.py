from flask import Flask, request, jsonify
from threading import Thread
from Data import Data

app = Flask(__name__)

mgr = Manager()


@app.route("/")
def root():
    return "aeon: saving your online time since 2019"


@app.route("/heatmap", methods=['POST'])
def update_heatmap():
    params = request.form
    new_data = params['data']
    video_id = params['videoId']
    result = mgr.updateHeatmap(video_id, new_data)
    return result


@app.route("/video/<video_id>", methods=['GET','POST'])
def get_video(video_id):
    video = mgr.findVideo(video_id)
    if video is not None:
        return jsonify(video)
    else:
        fetch_thread = Thread(target=mgr.analyze, kwargs={'id': video_id})
        fetch_thread.start()
        return "Video not found, getting"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
