# Spotify Playlist Downloader

This is a little script I wrote to download music stored in Spotify playlists from YouTube; I found it pretty useful when migrating to a non-streaming music library and figured others might as well.

# Usage

Create a Spotify API app here: https://developer.spotify.com/dashboard/applications. For convenience, set the redirect URI to http://localhost:8080, as this is the default setting in the script.

Then, run the script as:

```python3 main.py --client_id <client_id> --client_secret <client_secret> --username <username> --playlist <playlist name>```

# Requirements

* `youtube_dl==2020.6.16.1`
* `spotipy==2.13.0`
* `mutagen==1.45.0`
