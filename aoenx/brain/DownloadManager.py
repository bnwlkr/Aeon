import youtube_dl
import os

# Constants
yturl = "https://www.youtube.com/watch?v="
videoFileType = ".mp4"
tnFileType = ".jpg"
data = '../data/'


class DownloadManager:
    """
    Class for managing the downloading and deleting of video files used in
    analysis
    """
    def download(self, id):
        """
        Given a unique ID, download the YouTube video
        """
        url = yturl + id
        code = data + id + videoFileType

        if not os.path.isdir(data):
            os.makedirs(data)

        ydl_opts = {
            'outtmpl': code,
            'writethumbnail': True,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)

                title = info_dict.get('title', None)

                return title

        except Exception as e:
            print("Failed to download video: " + str(e))
            return None

    def delete(self, id):
        """
        Given a unique ID, delete the video file
        """
        try:
            os.remove(data + id + videoFileType)
            os.remove(data + id + tnFileType)
        except Exception as e:
            print("Failed to delete file: " + str(e))
