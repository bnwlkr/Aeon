from PIL import Image
from DownloadManager import DownloadManager, tnData, tnFileType, videoData, videoFileType
import numpy as np
from skimage.measure import compare_ssim as ssim
import os
import datetime
import time

class ThumbnailFinder:
    """
    A class for finding the closest key frame to the thumbnail
    """
    def find(self, id, fps):
        """
        The overall function for getting the best thumbnail
        """
        relPath = os.path.join(tnData, id + tnFileType)
        absPath = os.path.abspath(relPath)

        kf = self.getKeyFrames(absPath)

        sc = self.getSnapshots(kf, fps)

        if len(sc) > 0:
            tn = Image.open(relPath)
            tn = tn.convert("L")
            tn = np.asarray(tn)
            tn = tn.copy()

            def dist(im):
                im = im.convert("L")
                im = np.asarray(im)
                im = im.copy()
                im.thumbnail(tn.size)
                return np.dot(im, tn)

            vdist = np.vectorize(dist)

            dists = vdist(sc)

            ind = np.argmin(dists)

            return kf[ind]

        else:
            return None

    def getKeyFrames(self, path):
        """
        Use Microsoft Azure API to get the key frame timestamps
        """
        return []

    def getSnapshots(self, times, fps):
        """
        Produce the actual frames associated with the key frame timestamps
        """
        def frames(t):
            t = t.split(".")
            s = time.strptime(t[0],'%H:%M:%S')
            s = 60 * (60 * s.tm_hour + s.tm_min) + s.tm_sec
            s = s * 1000 + int(t[1])
            return s * fps

        vframes = np.vectorize(frames)

        inds = vframes(times)

        return []
