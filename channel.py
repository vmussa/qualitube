import requests
import json
from configparser import ConfigParser

configs = ConfigParser('config.ini')
API_KEY = configs['credentials']['api_key']

class Channel:
    def __init__(self, channel_id, api_key=API_KEY):
        self.channel_id = channel_id
        self.api_key = api_key

    def _parse_response(self, data):
        raw = json.loads(data)
        items = raw["items"]

        parsed = []
        for item in items:
            parsed.append({
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'published_at': item['snippet']['publishedAt'],
                'description': item['snippet']['description']
            })
        try:
            next_page_token = raw["nextPageToken"]
        except KeyError:
            next_page_token = False

        return parsed, next_page_token

    def get_videos_data(self, data=None, page_token=None):
        headers = {
            'Accept': 'application/json'
        }

        params = [
            ('part', 'snippet'),
            ('channelId', self.channel_id),
            ('key', self.api_key),
            ('maxResults', 50),
            ('type', 'video')
        ]

        if page_token:
            params.append(('pageToken', page_token))

        r = requests.get(
            'https://youtube.googleapis.com/youtube/v3/search',
            headers=headers,
            params=params
        )

        videos_data, next_page_token = self._parse_response(r.text)

        if next_page_token:
            return videos_data + self.get_videos_data(page_token=next_page_token)

        return videos_data
