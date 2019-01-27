import OpenCV
from PIL import Image
from DownloadManager import DownloadManager
import numpy as np

class ThumbnailFinder:
    """
    """
    def find(self, url):
        """
        """
        id = str(hash(url))
        path = id

        tn = im.open(os.path.join(tnData, id + tnFileType))

        kf = self.getKeyFrames(path)

        sc = self.getSnapshots(kf)

        def dist(im):
            return 0

        vdist = np.vectorize(dist)

        dists = vdist(sc)

        ind = np.argmin(dists)

        return kf[ind]

    def getKeyFrames(self, path):
        """
        """
        pass

    def getSnapshots(self, path):
        """
        """
        pass
