from spotify_api import (
    get_token,
    search_for_artist,
    get_songs_by_artist,
    get_related_artists,
)


def main():
    # get an access token
    token = get_token()

    # artist to search for
    artist_name = artist

    # search for an artist and retrieve their top songs
    artist_search_result = search_for_artist(token, artist_name)
    if artist_search_result is not None:
        artist_id = artist_search_result["id"]
        songs = get_songs_by_artist(token, artist_id)

        # print out each song's name
        # print("Top Songs:")
        # for idx, song in enumerate(songs):
        #     print(f"{idx + 1}. {song['name']}")

        # search for similar artist and display them
        similar_artists_search_result = get_related_artists(token, artist_id)
        if similar_artists_search_result is not None:
            similar_artists = similar_artists_search_result[:5]

            # print out each similar artist's name
            # print("Similar Artists:")
            # for idx, artist in enumerate(similar_artists):
            #     if artist["popularity"] >= 65:
            #         print(f"{artist['name']}")


if __name__ == "__main__":
    main()
