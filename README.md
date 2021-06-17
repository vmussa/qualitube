# qualitube
A Python package for YouTube qualitative data analysis. With this package you can download metadata and metrics from all videos from the given playlists' IDs. Every channel on YouTube has its own playlist with every single video uploaded by them. With this, you can take all the channels you want to study and extract their videos' data, generating a consistent `corpus`.

# Basic usage

## Installation

Create a virtual environment and install `qualitube` with pip:

```sh
pip install qualitube
```

Then, create a folder for your project. Inside it, take this repo's `config-sample.ini`, modify the sections so it has your YouTube Data API v3 credentials and the desired playlists' IDs. This should have the following format:

```ini
[credentials]
api_key=<PUT_HERE_YOUR_YOUTUBE_DATA_API_KEY>

[channels]
ids=
    <PUT_THE_PLAYLIST_ID_HERE>
    <PUT_ANOTHER_PLAYLIST_ID_HERE>
```

Inside this folder and with your `qualitube` virtual environment activated, simply run:

```sh
qualitube
```

You should see the pipeline logging messages. Your qualitative data should be in a `csv` file name `corpus.csv`. You can check if the pipeline has runned succesfully by looking at the `pipeline.log` generated log file too.