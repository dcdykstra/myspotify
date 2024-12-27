import json
import os
from datetime import datetime
import boto3

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def lambda_handler(event, context):
    print("getting boto3 client and parameters...")
    ssm = boto3.client("ssm")
    cache_param = ssm.get_parameter(Name="/spotify/auth_cache")
    cache_data = json.loads(cache_param["Parameter"]["Value"])

    print("saving to tmp/ folder...")
    print(f"{cache_data}")
    with open("/tmp/.cache", "w") as f:
        json.dump(cache_data, f)
    if os.path.exists("/tmp/.cache"):
        print("cache exists")

    print("authentication with spotipy...")
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
            redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
            scope="user-read-recently-played",
            cache_path="/tmp/.cache",
        )
    )
    print("saving recently played tracks...")
    results = sp.current_user_recently_played(limit=50)

    print("pulling relevant data...")
    tracks_data = []
    for item in results["items"]:
        track = item["track"]
        played_at = item["played_at"]

        track_info = {
            "track_name": track["name"],
            "track_id": track["id"],
            "artist_name": track["artists"][0]["name"],
            "artist_id": track["artists"][0]["id"],
            "duration_ms": track["duration_ms"],
            "popularity": track["popularity"],
            "played_at": played_at,
            "timestamp": datetime.now().isoformat(),
        }
        tracks_data.append(track_info)

    print("initializing connection to s3...")
    s3 = boto3.client("s3")

    filename = f"spotify_data/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

    print("uploading to s3...")
    s3.put_object(
        Bucket=os.environ["S3_BUCKET_NAME"], Key=filename, Body=json.dumps(tracks_data)
    )

    print("[ SUCCESS ]")
    return {
        "statusCode": 200,
        "body": json.dumps(f"Successfully processed {len(tracks_data)} tracks"),
    }
