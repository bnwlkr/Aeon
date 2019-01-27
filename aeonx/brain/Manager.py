from DownloadManager import DownloadManager
from ThumbnailFinder import ThumbnailFinder

class Manager:
    """
    Class for managing the analysis and management of video
    """
    def __init__(self):
        self.dlm = DownloadManager()
        self.tmf = ThumbnailFinder()
        #self.cmd = CommmentDownloader()
        #self.scf = SceneFinder()
        #self.hmf = HeatMapFinder()

    def analyze(self, id):
        """
        Do the full analysis of the video here
        """
        title, fps = self.dlm.download(id)

        if title is None:
            return {}

        thumbnail = self.tmf.find(id, fps)
        #comments = self.cmf.find(id)
        #heatmap = self.hmf.find(id)

        self.dlm.delete(id)

        obj = {
            'title': title,
            #'comments': comments,
            'thumbnail': thumbnail,
            #'scenes': scenes,
            #'heatmap': heatmap,
        }

        return obj


# To test, uncomment this and run the script or run this in a python terminal
m = Manager()
print(m.analyze("MEEJOZkmIxU"))
