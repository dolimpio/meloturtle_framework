import json
import os

import spotipy
from loguru import logger
from openai import OpenAI

from backend.services.recommendations_manager.recommendation_models.recommender_model import (
    RecommenderModel,
)


class ChatGPTAdapter(RecommenderModel):
    def __init__(self, config: dict):
        super().__init__(config)
        self.sp = None
        api_key = os.environ.get("BACKEND_CHATGTP_SECRET")
        if not api_key:
            logger.critical("OpenAI API key not found in environment variables.")
            raise ValueError("OpenAI API key is missing.")
        self.client = OpenAI(api_key=api_key)

    def initialize(self, access_token: str):
        """
        Initialize the model by authorizing the Spotify API.
        """
        try:
            self.sp = self.authorize(access_token)
            logger.info(f"{self.name} initialized and authorized with Spotify.")
        except Exception as e:
            logger.critical(f"Failed to authorize Spotify API: {e}")
            raise

    def finalize(self):
        """
        Finalize the model. For the ChatGPT API, there might not be much cleanup necessary.
        """
        self.sp = None
        logger.info(f"{self.name} finalized and cleaned up.")

    def generate_playlist(self, prompt: str, config: dict, context: dict) -> dict:
        """
        Generate a playlist based on the provided prompt, configuration, and context.

        Args:
            prompt (str): The input prompt for generating recommendations.
            config (dict): Additional configuration for the recommendation.
            context (dict): Contextual information.

        Returns:
            dict: A dictionary containing the prompt, configuration, and context with the Spotify playlist ID.
        """

        try:
            logger.info(f"Generating playlist with {self.name}...")

            if not json.loads(config.get("generate_genres")):
                genre_text = self.predict_genre(prompt)
                config["genres"] = genre_text
            else:
                genre_text = config.get("genres")

            logger.info(f"Genres: {genre_text}")
            params = self.generate_params(prompt, config.get("popularity"))
            logger.info(f"Params: {params}")
            tracks = self.recommend(
                params, genre_text, self.sp, config.get("num_songs")
            )
            logger.info(f"Playlist (Song URIs): {tracks}")
            spotify_id = self.create_spotify_playlist(tracks, prompt, self.sp)

            response = {
                "prompt": prompt,
                "config": config,
                "context": {"spotify_id": spotify_id},
            }

            return response

        except ValueError as e:
            print("ValueError:", e)
            logger.critical(e)
        except AttributeError as e:
            print("AttributeError:", e)
            logger.critical(e)
        except TypeError as e:
            print("TypeError:", e)
            logger.critical(e)
        except Exception as e:
            logger.info("exception cause" + e.__cause__)
            logger.info("exception context" + e.__context__)
            logger.info("exception dict" + e.__dict__)

            logger.critical(e)

    def authorize(self, access_token: str) -> spotipy.Spotify:
        """
        Create and return a Spotipy instance
        """
        return spotipy.Spotify(auth=access_token)

    def predict_genre(self, prompt: str) -> list:
        """
        Use OpenAI to predict music genres from the given prompt.
        """
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": 'I\'m a backend. You are a music genre selector critic. I will give you a text. You will extract Spotify music genres from it and give me a list of genres as an output like this example: ["rock", "pop", "rap"]. Add at least 3 and up to 5 genres in the list. Be selective and only add genres that really fit the mood of the text.  I will tip you if you make a good selection.  Keep the format of the output. These are the available genres: genres=["acoustic","afrobeat","alt-rock","alternative","ambient","anime","black-metal","bluegrass","blues","bossanova","brazil","breakbeat","british","cantopop","chicago-house","children","chill","classical","club","comedy","country","dance","dancehall","death-metal","deep-house","detroit-techno","disco","disney","drum-and-bass","dub","dubstep","edm","electro","electronic","emo","folk","forro","french","funk","garage","german","gospel","goth","grindcore","groove","grunge","guitar","happy","hard-rock","hardcore","hardstyle","heavy-metal","hip-hop","holidays","honky-tonk","house","idm","indian","indie","indie-pop","industrial","iranian","j-dance","j-idol","j-pop","j-rock","jazz","k-pop","kids","latin","latino","malay","mandopop","metal","metal-misc","metalcore","minimal-techno","movies","mpb","new-age","new-release","opera","pagode","party","philippines-opm","piano","pop","pop-film","post-dubstep","power-pop","progressive-house","psych-rock","punk","punk-rock","r-n-b","rainy-day","reggae","reggaeton","road-trip","rock","rock-n-roll","rockabilly","romance","sad","salsa","samba","sertanejo","show-tunes","singer-songwriter","ska","sleep","songwriter","soul","soundtracks","spanish","study","summer","swedish","synth-pop","tango","techno","trance","trip-hop","turkish","work-out","world-music",]',
                        },
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                },
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        logger.info(f"Response from OpenAI: {response.choices[0].message.content}")
        genres = json.loads(response.choices[0].message.content)
        logger.info(f"Genres to be passed to Spotify: {genres}")

        return genres

    def generate_params(self, prompt: str, popularity: int) -> dict:
        """
        Use OpenAI to generate Spotify song parameters from the given prompt.
        """
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": 'I\'m a backend. You\'re a music expert. I will give you a text. You\'ll extract Spotify song parameters from it and give me an output like this example: {"acousticness": 0.00242, "danceability": 0.585, "energy": 0.842, "instrumentalness": 0.00686, "key": 9, "liveness": 0.0866, "loudness": -5.883, "mode": 0, "speechiness": 0.0556, "tempo": 118.211, "time_signature": 4, "valence": 0.428}. Give me a value for all of them but make the values really fit the mood and emotion of the text. If the text doesnt make sense, still give me parameters. I will tip you if you make a good selection. Keep the format of the output.',
                        },
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                },
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        logger.info(f"Response from OpenAI: {response.choices[0].message.content}")
        parameters = json.loads(response.choices[0].message.content)
        audio_features = {"target_" + key: value for key, value in parameters.items()}
        audio_features["target_popularity"] = popularity
        logger.info(f"Converted to dictionary: {audio_features}")

        return audio_features

    def recommend(
        self, param_dict: dict, genre_list: list, sp: spotipy.Spotify, num_songs: int
    ) -> list:
        """
        Get Spotify recommendations based on the provided parameters and genres.
        """
        logger.info(f"Params for recommendation: {param_dict}")
        logger.info(f"Asked for this number of songs: {num_songs}")
        logger.info(f"This is the genre_list: {genre_list}")
        logger.info(f"This is the spotipy instance: {sp.me()}")

        result = sp.recommendations(
            seed_genres=genre_list, limit=num_songs, **param_dict
        )
        logger.info(
            f"This was the result for track recommendations from Spotify {result}."
        )

        if not result:
            logger.warning(f"Nothing was returned from Spotify for url {param_dict}.")
            raise Exception("Nothing returned from Spotify.")

        track_uris = [track["uri"] for track in result["tracks"]]

        return track_uris

    def create_spotify_playlist(
        self, track_uris: list, input_text: str, sp: spotipy.Spotify
    ) -> str:
        """
        Create a Spotify playlist with the given tracks for the current user.
        """
        # Define username and playlist name to generate
        user_id = sp.me()["id"]
        playlist_to_add = f"{input_text} - Meloturle generated"

        # Create playlist from given track URIs
        sp.user_playlist_create(user_id, playlist_to_add)

        playlists = sp.user_playlists(user_id)

        playlist_uid = playlists["items"][0]["id"]
        # Add tracks
        sp.playlist_add_items(playlist_uid, track_uris)
        logger.info(
            f"Spotify playlist '{playlist_to_add}' was created for user '{user_id}'."
        )

        return playlist_uid
