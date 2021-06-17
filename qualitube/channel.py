import requests
import json
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
API_KEY = config['credentials']['api_key']

class Channel:
    """
    A wrapper to get all videos' data from a given YouTube channel.
    """
    def __init__(self, channel_id, api_key=API_KEY):
        self.channel_id = channel_id
        self.api_key = api_key

    def _parse_response(self, data):
        """Parses the API 'Search: list' endpoint's JSON response for
        the retrieval of video metadata."""
        raw = json.loads(data)
        items = raw["items"]

        parsed = []
        for item in items:
            parsed.append({
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'published_at': item['snippet']['publishedAt']
            })
        try:
            next_page_token = raw["nextPageToken"]
        except KeyError:
            next_page_token = False

        return parsed, next_page_token

    def get_videos_data(self, page_token=None):
        """Uses the YouTube Data API v3 'Search: list' endpoint to get all
        videos from the Channel."""
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
