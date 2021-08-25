import requests
import json
import pandas as pd
from configparser import ConfigParser
from .log import logger
from .exceptions import QualitubeException


config = ConfigParser()
config.read("config.ini")
API_KEY = config['credentials']['api_key']


class PlaylistItems:
    """
    Wrapper class to the YouTube Data API v3's `PlaylistItems` endpoint
    with extra functionality.
    """
    def __init__(self, playlist_id, api_key=API_KEY):
        self.playlist_id = playlist_id
        self.api_key = api_key

    def _try_parse(self, item, key):
        try:
            parsed = item[key]
        except KeyError:
            logger.warn(
                f"YouTube Data API v3 does not provide the `{key}` parameter fo"
                f"r the requested playlist item. Setting it as `None`"
            )
            parsed = None
        return parsed
    
    def _parse_response(self, data):
        """Parses the API 'PlaylistItems: list' endpoint's JSON
        response for the retrieval of video metadata."""
        raw = json.loads(data)
        
        try:
            items = raw["items"]
        except KeyError:
            if "error" in raw.keys():
                raise QualitubeException(
                    f"\nAre you sure you set qualitube's config.ini file correctly?"
                    f"\nYou are getting the following error from YouTube's API response:"
                    f"\n\t{raw}"
                )
            raise

        parsed = []
        for item in items:
            parsed.append({
                'id': self._try_parse(item['contentDetails'], 'videoId'),
                'title': self._try_parse(item['snippet'], 'title'),
                'description': self._try_parse(item['snippet'], 'description'),
                'published_at': self._try_parse(item['snippet'], 'publishedAt')
            })
            logger.info(f"Got PlaylistItem -> id: {item['id']} / title: {item['snippet']['title']}")
        try:
            next_page_token = raw["nextPageToken"]
        except KeyError:
            next_page_token = False

        return parsed, next_page_token

    def get_playlist_items_data(self, page_token=None):
        """Uses the YouTube Data API v3 'PlaylistItems: list' endpoint 
        to get all videos from PlaylistItems (a youtube playlist)."""
        headers = {
            'Accept': 'application/json'
        }

        params = [
            ('part', ['contentDetails', 'snippet']),
            ('playlistId', self.playlist_id),
            ('key', self.api_key),
            ('maxResults', 50)
        ]

        if page_token:
            params.append(('pageToken', page_token))

        r = requests.get(
            'https://youtube.googleapis.com/youtube/v3/playlistItems',
            headers=headers,
            params=params
        )

        videos_data, next_page_token = self._parse_response(r.text)

        if next_page_token:
            return videos_data + self.get_playlist_items_data(page_token=next_page_token)

        return videos_data
    
    def to_df(self):
        data = self.get_playlist_items_data()
        df = pd.DataFrame(data)
        return df
