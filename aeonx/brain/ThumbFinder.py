from PIL import Image
from DownloadManager import DownloadManager, tnData, tnFileType, videoData, videoFileType
import numpy as np
from skimage.measure import compare_ssim as ssim
import os
import datetime
import time
import requests
import json

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

    ## REQUIRE: account_id and video_id, obtained by uploading video to indexer.
    def getKeyFrames(self, account_id, video_id):
        """
        Use Microsoft Azure API to get the key frame timestamps
        """
        #account_id = "78782446-d6cf-4dab-81b5-30a90ade9a9f"
        #video_id = "56187c4f2e"
        url = "https://api.videoindexer.ai/trial/Accounts/"+account_id+"/Videos/"+video_id+"/Index?language=English"
        
        count = 0;              # total number of keyframes
        keyTimes = []           # array of timestamps
        
        response = requests.get(url)
        print(response.status_code)
    
        video_data = json.loads(response.content.decode('utf-8'))
        
        #print times of key frames
        shots = video_data['videos'][0]['insights']['shots']
        
        # number of shots in data, each shot contains a number of keyFrames
        num_shots = len(video_data['videos'][0]['insights']['shots'])
        
        for i in range(0,num_shots):
            for key in shots[i]: 
                if key == 'keyFrames':
                    num_frames = len(shots[i]['keyFrames'])
                    for j in range(0, num_frames): 
                        keyTimes.append(shots[i]['keyFrames'][j]['instances'][0]['adjustedStart'])
                        count = count + 1
        return keyTimes


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
    

    
