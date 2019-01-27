from pymongo import MongoClient
from .brain.DownloadManager import DownloadManager
from .brain.Timestamps import Timestamps
from .brain.ThumbnailFinder import ThumbnailFinder


class Data():

    db_client = MongoClient()
    db = db_client['video_data']

    def find_video(self, video_id):
        video_collection = self.db['videos']
        return video_collection.find_one({'id': video_id})

    def update_heatmap(self, video_id, new_data):
        video = self.find_video(video_id)
        if video is None:
            return "heatmap not updated because video doesn't exist"
        else:
            heatmap = video['heatmap']
            index_flag = False
            for interval in new_data:
                start = interval['start']
                end = interval['end']
                for i in range(start, end):
                    try:
                        heatmap[i] += 1
                    except IndexError:
                        index_flag = True

            video_collection = self.db['videos']
            video_collection.update_one(
                {'id': video_id},
                {'$set': {
                    'heatmap': heatmap
                }}
            )

            if index_flag:
                return "heatmap updated with possible errors"
            else:
                return "heatmap successfully updated"

    def add_video(self, video_id):
        title, fps = DownloadManager.download(video_id)
        if title is not None:
            comments = Timestamps.parse_comments(video_id=video_id, num_pages=50)
            thumb = ThumbnailFinder.find(video_id, fps)
            video = {
                'id': video_id,
                'title': title,
                'comments': comments,
                'thumbnail': thumb,
                'scenes': [],
                'heatmap': [],
            }
            video_collection = self.db['videos']
            new_id = video_collection.insert_one(video).inserted_id
            print(new_id)
