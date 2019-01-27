from pymongo import MongoClient
from brain.DownloadManager import DownloadManager
from brain.Timestamps import Timestamps
from pymongo.errors import DuplicateKeyError
#from .brain.ThumbnailFinder import ThumbnailFinder


class Data():

    URI = "mongodb://aeonmongo:0RMcFPsiTtjJ0drUtntVtPoD0PZ90dzOOD6e2hOKuzjXYhlU1BSIapsU8uZi1f7a9M2qGefjDVcpupKFgl06Lg==@aeonmongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
    db_client = MongoClient(URI)
    db = db_client['video_data']

    def find_video(self, video_id):
        video_collection = self.db['videos']
        return video_collection.find_one({'_id': video_id})

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
        dl = DownloadManager()
        title, fps = dl.download(id=video_id)
        if title is not None:
            comments = Timestamps.parse_comments(video_id=video_id, num_pages=50)
            video = {
                '_id': video_id,
                'title': title,
                'comments': comments,
                #'thumbnail': thumb,
                'scenes': [],
                'heatmap': [],
            }
            video_collection = self.db['videos']
            try:
                new_id = video_collection.insert_one(video).inserted_id
                print("[timestamps] inserted video: " + str(new_id))
            except DuplicateKeyError:
                print("[timestamps] video was already added")
