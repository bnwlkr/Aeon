from brain.DownloadManager import DownloadManager
from brain.ThumbnailFinder import ThumbnailFinder
from brain.Data import Data
from brain.Timestamps import Timestamps

class Manager:
    """
    Class for managing the analysis and management of video
    """
    def __init__(self):
        self.dlm = DownloadManager()
        self.tmf = ThumbnailFinder()
        self.data = Data()
        #self.scf = SceneFinder()

    def analyze(self, id):
        """
        Do the full analysis of the video here
        """
        title, length, shape = self.dlm.download(id)

        if title is None:
            return {}

        thumbnail = self.tmf.find(id, shape)
        comments = Timestamps.parse_comments(video_id=id, num_pages=50)

        self.dlm.delete(id)

        obj = {
            '_id': id,
            'title': title,
            'comments': comments,
            'thumbnail': thumbnail,
            #'scenes': scenes,
            'heatmap': [0]*length
        }

        self.data.add_video(obj)

        return obj

    def updateHeatmap(self, video_id, new_data):
        return self.data.update_heatmap(video_id, new_data)

    def findVideo(self, video_id):
        return self.data.find_video(video_id)
