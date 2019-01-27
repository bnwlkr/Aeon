from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class Data:

    URI = "mongodb://aeonmongo:0RMcFPsiTtjJ0drUtntVtPoD0PZ90dzOOD6e" \
          "2hOKuzjXYhlU1BSIapsU8uZi1f7a9M2qGefjDVcpupKFgl06Lg==@aeo" \
          "nmongo.documents.azure.com:10255/?ssl=true&replicaSet=gl" \
          "obaldb"

    db_client = MongoClient(URI)
    db = db_client['video_data']

    def find_video(self, video_id):
        video_collection = self.db['videos']
        return video_collection.find_one({'_id': video_id})

    def update_heatmap(self, video_id, new_data):
        print(video_id)
        print(new_data)
        video = self.find_video(video_id)
        if video is None:
            return "heatmap not updated because video doesn't exist"
        else:
            heatmap = video['heatmap']
            index_flag = False
            for second in new_data:
                try:
                    heatmap[int(second)] += 1
                except IndexError:
                    index_flag = True

            video_collection = self.db['videos']
            video_collection.update_one(
                {'_id': video_id},
                {'$set': {'heatmap': heatmap }}
            )

            if index_flag:
                return "heatmap updated with possible errors"
            else:
                return "heatmap successfully updated"

    def add_video(self, video):
        video_collection = self.db['videos']
        try:
            new_id = video_collection.insert_one(video).inserted_id
            print("[timestamps] inserted video: " + str(new_id))
        except DuplicateKeyError:
            print("[timestamps] video was already added")
