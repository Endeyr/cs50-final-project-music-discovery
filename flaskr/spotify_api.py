# import necessary modules
from dotenv import load_dotenv
import os
import base64
from requests import get, post

# load Spotify API keys from .env file
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# get access token from Spotify API
def get_token():
    # create authorization string used in header
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    # send post request to retrieve token
    result = post(url, headers=headers, data=data)
    result.raise_for_status()
    json_result = result.json()

    # return the access token from the response body
    token = json_result["access_token"]
    return token


# create Authorization header containing the access token
def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}


# search for an artist by name and return the first result if found
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    # Allowed values: "album", "artist", "playlist", "track", "show", "episode", "audiobook" separated by commas
    type = "artist"
    limit = 1
    query = f"?q={artist_name}&type={type}&limit={limit}"
    query_url = f"{url}{query}"

    # send GET request to retrieve artist information
    result = get(query_url, headers=headers)
    result.raise_for_status()
    json_result = result.json()["artists"]["items"]

    # if no artist is found, return None
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None

    # return the first artist result
    return json_result[0]


# retrieve top tracks for a given artist ID
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = get_auth_header(token)

    # send GET request to retrieve list of songs
    result = get(url, headers=headers)
    result.raise_for_status()
    json_result = result.json()["tracks"]

    # return list of songs
    return json_result

# retrieve artist albums
def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album&market=US"
    headers = get_auth_header(token)

    # send GET request to retrieve list of albums
    result = get(url, headers=headers)
    result.raise_for_status()
    json_result = result.json()["items"]

    # return list of albums
    return json_result

# retrieve related artist
def get_related_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = get_auth_header(token)

    # send GET request to retrieve list of songs
    result = get(url, headers=headers)
    result.raise_for_status()
    json_result = result.json()["artists"]

    # return list of songs
    return json_result

__all__ = [
    "get_token",
    "search_for_artist",
    "get_songs_by_artist",
    "get_related_artists",
]
