from PIL import Image
from brain.DownloadManager import tnData, tnFileType, videoData, videoFileType
import numpy as np
import os
import subprocess

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

        output = os.path.join("data", id + ".txt")
        cmd = "ffmpeg -i " + os.path.join(videoData, id) + ".mp4 -loop 1 -i " \
              + os.path.join(tnData, id) \
              + '.jpg -an -filter_complex "blend=difference:shortest=1,blackframe=99:128" -f null - > ' \
              + output + ' 2>&1'

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
            try:
                tn = round(np.argmax(count) / fps)
            except ValueError:
                print("[thumbnail] thumbnail could not be located")
                tn = None

        os.remove(output)

        return tn
