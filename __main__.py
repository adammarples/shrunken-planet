from dataclasses import dataclass
from pprint import pprint
import datetime
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import dotenv

from scrape import list_feeds


dotenv.load_dotenv(".spotify", override=True)


def make_token():
    return spotipy.util.prompt_for_user_token("adammarples", "playlist-modify-public",)


@dataclass
class Spotify:
    username = "adammarples"
    client = spotipy.Spotify(auth=make_token())


def search_for_uri(track):
    try:
        results = Spotify.client.search(q=f"{track.artist} {track.name}")
        items = list(results.values())[0]["items"]
    except spotipy.client.SpotifyException:
        return
    if not items:
        return
    item = items.pop()
    print(track)
    return item["uri"]


if __name__ == "__main__":
    playlists = Spotify.client.user_playlists(Spotify.username)["items"]
    playlist_titles = [playlist["name"] for playlist in playlists]
    for feed in list_feeds():
        print(f"{feed.title}")
        if feed.title not in playlist_titles:
            playlist = Spotify.client.user_playlist_create(Spotify.username, feed.title)
            uris = [search_for_uri(track) for track in feed.tracks]
            uris = [uri for uri in uris if uri is not None]
            Spotify.client.user_playlist_add_tracks(
                Spotify.username, playlist["id"], uris, position=None
            )
