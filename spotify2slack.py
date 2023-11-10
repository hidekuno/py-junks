#!/usr/bin/env python
#
# this is toy tool
#
import os
import spotipy
from slack_sdk.webhook import WebhookClient

CLIENT_ID = os.environ["S2S_CLIENT_ID"]
CLIENT_SECRET = os.environ["S2S_CLIENT_SECRET"]
SPOTIFY_DEV_URI = os.environ["S2S_SPOTIFY_DEV_URI"]
WEBHOOK_URL = os.environ["S2S_WEBHOOK_URL"]
USERNAME = os.environ["S2S_USERNAME"]

client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
    CLIENT_ID, CLIENT_SECRET
)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

token = spotipy.util.prompt_for_user_token(
    username=USERNAME,
    scope="user-read-currently-playing",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=SPOTIFY_DEV_URI,
)
spotify = spotipy.Spotify(auth=token)
current_playing = spotify.current_user_playing_track()
spotify_url = current_playing["item"]["album"]["external_urls"]["spotify"]

webhook = WebhookClient(WEBHOOK_URL)
response = webhook.send(text=spotify_url)

if response.status_code != 200:
    print(response)
