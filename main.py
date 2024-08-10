import pandas as pd
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from src.pull.mySpotifyClient import mySpotifyClient
from src.helper.cleaner import FileCleaner
from src.config.config import config
from src.config.config import day


def main():
    spot = mySpotifyClient()

    spot.save_n_playlist_tracks_b50("4gN7NFxZIBsY8cn264qfx3")


if __name__ == "__main__":
    main()
