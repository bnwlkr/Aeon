from DownloadManager import DownloadManager
from ThumbnailFinder import ThumbnailFinder
from Data import Data
from Timestamps import Timestamps
import subprocess

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
        title, shape = self.dlm.download(id)

        if title is None:
            return {}

        thumbnail = self.tmf.find(id, shape)
        comments = Timestamps.parse_comments(video_id=id, num_pages=50)

        self.dlm.delete(id)

        obj = {
            'id': id,
            'title': title,
            'comments': comments,
            'thumbnail': thumbnail,
            #'scenes': scenes,
        }

        self.data.add_video(obj)

        return obj

    def updateHeatmap(video_id, new_data):
        return self.data.update_heatmap(video_id, new_data)

    def findVideo(video_id):
        return self.data.find_video(video_id)
