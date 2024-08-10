import pandas as pd
import numpy as np
import json
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from src.config.config import config
from src.config.config import day
from src.config.config import mkdir_ifnotexist


class mySpotifyClient:
    def __init__(self) -> None:
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=config.client_id,
                client_secret=config.client_secret,
                redirect_uri=config.redirect_uri,
                scope="user-library-read",
            )
        )
        self.user = self.sp.user(config.spotify_user)

    def save_n_liked_tracks_b50(self, n_tracks=7000):
        for i in range(n_tracks // 50 + 1):
            results = self.sp.current_user_saved_tracks(limit=50, offset=i * 50)
            if results["items"] != []:
                with open(
                    config.outputdir + f"/json/tracks/saved_tracks_b50_{i}.json", "w"
                ) as f:
                    json.dump(results, f)
            else:
                break

    def save_n_playlists_b50(self, n_playlists=500):
        for i in range(n_playlists // 50 + 1):
            results = self.sp.user_playlists(
                config.spotify_user, limit=50, offset=i * 50
            )
            if results["items"] != []:
                with open(
                    config.outputdir + f"/json/playlists/user_playlists_b50_{i}.json",
                    "w",
                ) as f:
                    json.dump(results, f)
            else:
                break

    def save_n_playlist_tracks_b50(self, playlist_id, n_tracks=1000):
        for i in range(n_tracks // 100 + 1):
            results = self.sp.playlist_items(playlist_id, limit=100, offset=i * 100)
            if results["items"] != []:
                playlistFolderPath = os.path.join(
                    config.outputdir, f"json/playlist_tracks/{playlist_id}"
                )
                mkdir_ifnotexist(playlistFolderPath)

                with open(
                    os.path.join(playlistFolderPath, f"playlist_tracks_b100_{i}.json"),
                    "w",
                ) as f:
                    json.dump(results, f)
            else:
                break
