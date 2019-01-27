import youtube_dl
import os

# Constants
ytUrl = "https://www.youtube.com/watch?v="
videoFileType = ".mp4"
tnFileType = ".jpg"
videoData = os.path.join('data', 'videos')
tnData = os.path.join('data', 'thumbnails')


class DownloadManager:
    """
    Class for managing the downloading and deleting of video files used in
    analysis
    """
    def download(self, id):
        """
        Given a unique ID, download the YouTube video
        """
        url = ytUrl + id

        if not os.path.isdir(videoData):
            os.makedirs(videoData)

        if not os.path.isdir(tnData):
            os.makedirs(tnData)

        self.delete(id)

        ydl_opts = {
            'outtmpl': os.path.join(videoData, id + videoFileType),
            'format': 'mp4',
            'writethumbnail': True,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)

                title = info_dict.get('title', None)
                width = info_dict.get('width', None)
                height = info_dict.get('height', None)
                length = info_dict.get('duration', None)

                os.rename(os.path.join(videoData, id + tnFileType), os.path.join(tnData, id + tnFileType))

                return title, length, (width, height)

        except Exception as e:
            print("Failed to download video: " + str(e))
            return None, None, None

    def delete(self, id):
        """
        Given a unique ID, delete the video file
        """
        try:
            os.remove(os.path.join(videoData, id + videoFileType))
            os.remove(os.path.join(tnData, id + tnFileType))
        except Exception as e:
            print("Failed to delete file: " + str(e))
