from DownloadManager import DownloadManager

class Manager:
    """
    Class for managing the analysis and management of video
    """
    def __init__(self):
        self.dlm = DownloadManager()
        #self.tmf = ThumbFinder()
        #self.cmf = CommmentFinder()
        #self.scf = SceneFinder()
        #self.hmf = HeatMapFinder()

    def analyze(self, id):
        """
        Do the full analysis of the video here
        """
        title = self.dlm.download(id)

        #thumbnail = self.tmf.find(id)
        #comments = self.cmf.find(id)
        #scenes = self.scf.find(id)
        #heatmap = self.hmf.find(id)

        self.dlm.delete(id)

        obj = {
            'title': title,
            #'comments': comments,
            #'thumbnail': thumbnail,
            #'scenes': scenes,
            #'heatmap': heatmap,
        }

        return obj


# To test, uncomment this and run the script
#m = Manager()
#print(m.analyze("MEEJOZkmIxU"))
