from urllib.parse import urlencode
from urllib.request import urlopen, Request
import json
import re

timestamp_ex = re.compile("\d{1,2}:\d{2}")
minutes_ex = re.compile("\d{1,2}:")


class CommentDownloader:

    @staticmethod
    def load_api_key():
        key_file = open('apikey.txt', 'rb')
        api_key = str(key_file.read().decode('utf-8'))
        key_file.close()
        return api_key

    @staticmethod
    def parse_for_timestamp(data):
        time_match = timestamp_ex.search(data);
        if time_match is not None:
            time = time_match.group()
            min_match = minutes_ex.match(time)
            min_data = min_match.group()
            min = int(min_data[0:len(min_data) - 1])
            second_start = min_match.end()
            sec = int(time[second_start:])
            ts = (min * 60) + sec
            return ts

        return None

    @staticmethod
    def get_comments_thread_by_video_id(video_id, num, key, next_page):
        url = "https://www.googleapis.com/youtube/v3/commentThreads"
        params = {
            'key': key,
            'textFormat': "plainText",
            'part': "snippet",
            'videoId': video_id,
            'maxResults': num,
        }

        if next_page is not None:
            params['pageToken'] = next_page

        request = Request(url + '?' + urlencode(params))
        response = urlopen(request)
        response_string = response.read().decode('utf-8')
        comments_data = json.loads(response_string)
        num_results = comments_data['pageInfo']['totalResults']
        comments_items = comments_data['items']
        results = []
        for ix in range(0,num_results):
            comment = comments_items[ix]
            data = comment['snippet']['topLevelComment']['snippet']['textDisplay']
            time = CommentDownloader.parse_for_timestamp(data=data)
            if time is not None:
                result = {}
                result[time] = data
                results.append(result)
        next_page_token = comments_data['nextPageToken']
        return results, next_page_token

    @staticmethod
    def download(video_id, num_pages):
        key = CommentDownloader.load_api_key()
        results, ts = CommentDownloader.get_comments_thread_by_video_id(video_id=video_id, num=100, key=key, next_page=None)
        pages_done = 1
        while ts and pages_done < num_pages:
            new_results, ts = CommentDownloader.get_comments_thread_by_video_id(video_id=video_id, num=100, key=key, next_page=ts)
            results += new_results
            pages_done += 1

        return results

dl = CommentDownloader()
results = dl.download('kffacxfA7G4', 10)
print(results)
