from PIL import Image
from DownloadManager import DownloadManager, tnData, tnFileType, videoData, videoFileType
import numpy as np
from skimage.measure import compare_ssim as ssim
import os
import subprocess
import math

class ThumbnailFinder:
    """
    A class for finding the closest key frame to the thumbnail
    """
    def find(self, id, shape):
        """
        The overall function for getting the best thumbnail
        """
        relTnPath = os.path.join(tnData, id + tnFileType)
        relVidPath = os.path.join(videoData, id + videoFileType)

        im = Image.open(relTnPath)
        im = im.resize(shape)
        os.remove(relTnPath)
        im.save(relTnPath)

        output = "..\\data\\" + id + ".txt"
        cmd = "ffmpeg.exe -i ..\\data\\videos\\" + id + ".mp4 -loop 1 -i ..\\data\\thumbnails\\" + id + '.jpg -an -filter_complex "blend=difference:shortest=1,blackframe=99:128" -f null - > ' + output + ' 2>&1'
        print(cmd)
        ps = subprocess.Popen(cmd, shell=True)
        ps.wait()

        tn = None

        with open(output) as file:
            lines = file.readlines()
            fpsls = [l for l in lines if "Stream #0" in l]
            fpsls = fpsls[0]
            fpsls = fpsls[:fpsls.find(" fps,")]
            fpsls = fpsls[fpsls.rfind(" ") + 1:]
            fps = float(fpsls)
            frame = [l for l in lines if "[Parsed_blackframe_1 @" in l]
            frame = [l[l.find(" frame:") + 7:] for l in frame]
            frame = [(round(int(l[:l.find(" ")]) / 100) + 0.5) * 100 for l in frame]
            count = np.bincount(frame)
            tn = round(np.argmax(count) / fps, 2)

        os.remove(output)

        return tn
