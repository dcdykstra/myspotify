"""
Config INI helpers and Logging helper
"""

import logging
import os
from datetime import date, timedelta

from tokenize import String
from configparser import ConfigParser


class ConfigIni:
    """Gets information from config.ini file"""

    def __init__(self) -> None:
        path = os.path.dirname(os.path.abspath(__file__))
        local_config = ConfigParser()
        local_config.read(os.path.join(path, "config.ini"))
        userinfo = local_config["USERINFO"]
        self.client_id = userinfo["client_id"]
        self.client_secret = userinfo["client_secret"]
        self.outputdir = userinfo["outputdir"]
        self.redirect_uri = userinfo["redirect_uri"]
        self.spotify_user = userinfo["spotify_user"]
        self.daysago = 0


def mkdir_ifnotexist(path: str):
    """Created the folder if it doesn't exist"""
    if not os.path.exists(path):
        os.mkdir(path)


def clear_dir(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


# Create data output folders based on config
config = ConfigIni()
mkdir_ifnotexist(config.outputdir)

jsonFolderPath = os.path.join(config.outputdir, "json")
mkdir_ifnotexist(jsonFolderPath)
playlistFolderPath = os.path.join(jsonFolderPath, "playlists")
mkdir_ifnotexist(playlistFolderPath)
tracksFolderPath = os.path.join(jsonFolderPath, "tracks")
mkdir_ifnotexist(tracksFolderPath)
playlistTracksFolderPath = os.path.join(jsonFolderPath, "playlist_tracks")
mkdir_ifnotexist(playlistTracksFolderPath)

outputFolderPath = os.path.join(config.outputdir, "output")
mkdir_ifnotexist(outputFolderPath)
clear_dir(outputFolderPath)

# Creating day for naming
day = date.today() - timedelta(days=config.daysago)
day = day.strftime("%Y-%m-%d")
