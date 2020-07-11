import argparse
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.util import prompt_for_user_token

from youtube_utils import YoutubeSearch, DownloadOpts
import youtube_dl

parser = argparse.ArgumentParser()
parser.add_argument('--client_id', help='Spotify API client ID')
parser.add_argument('--client_secret', help='Spotify API client secret')
parser.add_argument('--redirect_uri', default='http://localhost:8080', help='Spotify API redirect URI')
parser.add_argument('--username', help='Spotify username')
parser.add_argument('--playlist', help='Spotify playlist name')
parser.add_argument('--output', help='output directory')
opt = parser.parse_args()
print(opt)

def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_playlist_id(username, playlist_name):
    playlists = sp.user_playlists(username)
    while playlists:
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                return playlist['uri']
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

if __name__ == "__main__":
    url_prefix = 'https://www.youtube.com'
    scope = "user-library-read playlist-read-private"

    if opt.output is None:
        if not os.path.isdir(opt.playlist):
            os.mkdir(opt.playlist)
        DownloadOpts['outtmpl'] = './{}/%(title)s.%(ext)s'.format(opt.playlist)
    else:
        DownloadOpts['outtmpl'] = './{}/%(title)s.%(ext)s'.format(opt.output)

    token = prompt_for_user_token(client_id=opt.client_id,
                                  client_secret=opt.client_secret,
                                  redirect_uri=opt.redirect_uri,
                                  username=opt.username,
                                  scope=scope)

    if token:
       sp = spotipy.Spotify(auth=token)

    playlist_id = get_playlist_id(opt.username, opt.playlist)
    playlist_tracks = get_playlist_tracks(opt.username, playlist_id)

    query_terms = [track['track']['artists'][0]['name'] + ' ' + track['track']['name'] for track in playlist_tracks]

    for query in query_terms:
        query_results = YoutubeSearch(query, max_results=1).to_dict()
        url_suffix = query_results[0]['url_suffix']

        with youtube_dl.YoutubeDL(DownloadOpts) as ydl:
           ydl.download([url_prefix + url_suffix])
