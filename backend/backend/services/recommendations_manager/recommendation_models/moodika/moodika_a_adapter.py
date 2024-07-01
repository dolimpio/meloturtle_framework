import json

from loguru import logger

from backend.services.recommendations_manager.recommendation_models.moodika.model_a.moodika import *
from backend.services.recommendations_manager.recommendation_models.recommender_model import (
    RecommenderModel,
)

class MoodikaAAdapter(RecommenderModel):
    def __init__(self, model_config: dict):
        super().__init__(model_config)
        self.sp = None

    def initialize(self, access_token: str):
        """
        Initialize the MoodikaAAdapter by authorizing the Spotify API.

        :param access_token: Spotify access token for authorization.
        """
        try:
            self.sp = authorize(access_token)
            logger.info(f"{self.name} initialized and authorized with Spotify.")
        except Exception as e:
            logger.critical(f"Failed to authorize Spotify API: {e}")
            raise

    def generate_playlist(self, prompt: str, config: dict, context: dict) -> dict:
        """
        Generate a playlist based on the given prompt, configuration, and context.

        :param prompt: The input prompt for generating the playlist.
        :param config: Configuration dictionary for generating the playlist.
        :param context: Context dictionary.
        :return: A dictionary containing the generated playlist details.
        """
        try:
            logger.info(f"Generating playlist with {self.name}...")

            if not json.loads(config.get("generate_genres")):
                genre_text = predict_genre(prompt)
                config["genres"] = genre_text
            else:
                genre_text = config.get("genres")

            logger.info("\nGenres:" + str(genre_text))
            params = generate_params(prompt, 20, self.sp, config.get("popularity"))
            logger.info("\nParams:" + str(params))
            tracks = recommend(params, genre_text, self.sp, config.get("num_songs"))
            spotify_id = create_spotify_playlist(tracks, prompt, self.sp)

            response = {
                "prompt": prompt,
                "config": config,
                "context": {"spotify_id": spotify_id},
            }

            return response

        except ValueError as e:
            print("ValueError:", e)
            logging.critical(e)
        except AttributeError as e:
            print("AttributeError:", e)
            logging.critical(e)
        except TypeError as e:
            print("TypeError:", e)
            logging.critical(e)
        except Exception as e:
            logging.critical(e)

    def finalize(self):
        """
        Finalize the MoodikaAAdapter. Perform any necessary cleanup.
        """
        self.sp = None
        logging.info(f"{self.name} finalized and cleaned up.")
