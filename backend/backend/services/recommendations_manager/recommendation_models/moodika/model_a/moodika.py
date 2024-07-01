import logging

import numpy as np
import pandas as pd
import spotipy
from sentence_transformers import CrossEncoder

from backend.services.recommendations_manager.recommendation_models.moodika.model_a import (
    config as cfg,
)

logging.basicConfig(
    filename=cfg.LOGFILE_NAME,
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
)


def authorize(access_token: str):
    """
    Create and return a Spotipy instance
    """
    sp = spotipy.Spotify(auth=access_token)
    return sp


def predict_genre(prompt):
    """
    Takes given free text and returns the most similar genres over a given similarity threshold (limit 5).
    Threshold can be configured in config file.
    If no genres are found over similarity threshold, a default list of genres is returned (can be configured as well).
    """

    similarity_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    # We want to compute the similarity between the query sentence
    input_text = prompt

    # Take all combinations of the text and genre
    genres = cfg.genres
    sentence_combinations = [[input_text, genre] for genre in genres]

    # find the similarity scores between the text and each genre, and sort from highest to lowest
    similarity_scores = similarity_model.predict(sentence_combinations)
    sim_scores_sorted = reversed(np.argsort(similarity_scores))

    # Return the top genres over a given threshold
    top_genres = []
    top_scores = []
    for idx in sim_scores_sorted:
        print("{:.2f}\t{}".format(similarity_scores[idx], genres[idx]))
        if len(top_genres) < 5:
            top_genres.append(genres[idx])
            top_scores.append(similarity_scores[idx])

    for i in range(len(top_scores) - 1):
        if abs(top_scores[i + 1]) - abs(top_scores[i]) > 2:
            top_genres = top_genres[: i + 1]
            break

    # take only the top 5 genres
    print(f"Genres to be passed to Spotify: {top_genres}")
    return top_genres


def recommend(param_dict, genre_list, sp, num_songs):
    """
    Takes a dictionary of values for various audio parameters and returns a list of Spotify-recommended track URIs.
    """
    # Send a request to Spotify API using Spotipy
    result = sp.recommendations(seed_genres=genre_list, limit=num_songs, **param_dict)

    # Iterate over response from Spotify, taking track URIs from recommended tracks
    if result:
        track_uris = []
        print("Playlist")
        for track in result["tracks"]:
            # print(f"Song: {track['name']}, Artist: {dict(track['album']['artists'][0])['name']}\n")
            track_uris.append(track["uri"])
    else:
        logging.warning(f"Nothing was returned from Spotify for url {param_dict}.")
        raise Exception("Nothing returned from Spotify.")
    return track_uris


def create_spotify_playlist(track_uris, input_text, sp):
    """
    Utilize Spotipy library to create a playlist given list of track URIs for current user
    """
    # Define username and playlist name to generate
    user_id = sp.me()["id"]
    print("userid" + user_id)

    playlist_to_add = f"{input_text} - Meloturle generated"

    # Create playlist from given track URIs
    sp.user_playlist_create(user_id, playlist_to_add)
    print("inside create_spotify_playlist")

    playlists = sp.user_playlists(user_id)

    playlist_uid = playlists["items"][0]["id"]
    playlist_link = f"https://open.spotify.com/playlist/{playlist_uid}"
    # print(f"Track URIs: {track_uris}")

    # Add tracks
    sp.playlist_add_items(playlist_uid, track_uris)
    logging.info(
        f"Spotify playlist '{playlist_to_add}' was created for Spotify user '{user_id}'.",
    )

    print(f"User ID: {user_id}")
    print(f"Playlist name: {playlist_to_add}")
    print(f"Playlist link: {playlist_link}")
    # MODIFIED to return id
    return playlist_uid


def raise_spotify_error():
    """
    Raise exception if no result is found from Spotify search (should be relatively rare)
    """
    raise Exception(f"Nothing Returned from Spotify. Try using different input.")


def generate_params(prompt, num_playlists, sp, popularity):
    """
    Generate parameters from given text.
    Process is as follows:
    1. Search Spotify playlists for given text and return number of playlists given in num_playlists
    2. Return all tracks for each playlist, removing tracks that are of NoneType
    3. Find each audio feature for each song -
        then average for each audio feature across entire playlist for each playlist
    4. Average the averages for each playlist, return a dictionary of average for each audio feature
    """
    try:
        # Save text argument and initialize a Spotipy instance
        input_text = prompt
        # sp = authorize()
        # (1) Get all playlist uris from playlists in search results
        playlists_results = sp.search(
            q=input_text, limit=num_playlists, type="playlist"
        )["playlists"]
        print("inside generate_params")

        playlist_uris = [playlist["id"] for playlist in playlists_results["items"]]
        print("Playlist URIs (list of strings):", playlist_uris, "\n")

        # (2) Get all track uris from playlists in search results
        track_results = [sp.playlist_items(p_uri, limit=100) for p_uri in playlist_uris]
        if len(track_results) == 0:
            raise_spotify_error()

        # Make sure to remove NoneTypes
        track_uris_dict = {
            playlist_uris[i]: [
                track["track"]["id"] if track["track"] is not None else None
                for track in track_results[i]["items"]
            ]
            for i in range(len(playlist_uris))
        }
        track_uris_dict = {
            key: [track_uri for track_uri in track_uris_dict[key] if track_uri]
            for key in track_uris_dict
        }
        # print("Track URIs (dict):\n", track_uris_dict)

        # (3) Get audio features of each track in each playlist
        audio_features = [
            sp.audio_features(tracks=track_uris_dict[playlist])
            for playlist in track_uris_dict
        ]

        # (4) Average playlist averages to get average audio features for individual search
        audio_features = [
            [track_features for track_features in playlist if track_features]
            for playlist in audio_features
        ]
        # print("Audio Features (list of ):\n", audio_features)

        # Build dictionary of averages
        audio_features = [
            [{f: track[f] for f in cfg.AUDIO_FEATURES_TO_EXTRACT} for track in playlist]
            for playlist in audio_features
        ]
        avg_audio_features = dict(
            pd.concat(
                [
                    pd.DataFrame(audio_features[i]).mean()
                    for i in range(len(playlist_uris))
                ],
                axis=1,
            ).mean(axis=1),
        )

        # Add popularity given to parameter dictionary
        avg_audio_features["popularity"] = popularity
        print("Features averaged (series):\n", avg_audio_features, "\n")
    except Exception as e:
        logging.info("exception cause MOODIKA" + str(e.__cause__))
        logging.info("exception context MOODIKA" + str(e.__context__))
        logging.info("exception dict MOODIKA" + str(e.__dict__))
        logging.info("exception dict MOODIKA" + str(e))

        logging.critical(e)

    return avg_audio_features
