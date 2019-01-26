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

    def analyze(self, url):
        """
        Do the full analysis of the video here
        """
        title = self.dlm.download(url)

        #thumbnail = self.tmf.find(url)
        #comments = self.cmf.find(url)
        #scenes = self.scf.find(url)
        #heatmap = self.hmf.find(url)

        self.dlm.delete(url)

        obj = {
            'title': title,
            #'comments': comments,
            #'thumbnail': thumbnail,
            #'scenes': scenes,
            #'heatmap': heatmap,
        }

        return obj


# To test, uncomment this and run the script or run this in a python terminal
#m = Manager()
#print(m.analyze("https://www.youtube.com/watch?v=MEEJOZkmIxU"))
