from .playlist_items import PlaylistItems
from configparser import ConfigParser
from .videos import Videos
import pandas as pd
import logging
import sys

config = ConfigParser()
config.read("config.ini")
CHANNEL_IDS = config['channels']['ids'].split("\n")[1:]

def get_playlist_items_objs(channel_ids: str) -> PlaylistItems:
    """Get list of PlaylistItems objects from channel ids."""
    objs = [PlaylistItems(channel_id) for channel_id in channel_ids]
    return objs

def chunks(lst: list, n) -> list:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main():
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler('pipeline.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info('Beginning of pipeline.')

    playlists = get_playlist_items_objs(channel_ids=CHANNEL_IDS)
    dfs = [playlist.to_df() for playlist in playlists]
    raw = pd.concat(dfs)
    videos_ids_lst = raw['id'].to_list()
    chunked = list(chunks(videos_ids_lst, 50))

    dfs = []
    for chunk in chunked:
        dfs.append(Videos(chunk).to_df())

    df = pd.concat(dfs).reset_index(drop=True)
    df.to_csv('corpus.csv', index=False)

    logging.info('End of pipeline.')

if __name__ == "__main__":
    main()
