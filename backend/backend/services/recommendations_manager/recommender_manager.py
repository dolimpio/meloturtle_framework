from typing import Dict, List

from backend.services.recommendations_manager.recommendation_models.chatgpt.chatgpt_adapter import (
    ChatGPTAdapter,
)
from backend.services.recommendations_manager.recommendation_models.moodika.moodika_a_adapter import (
    MoodikaAAdapter,
)
from backend.services.recommendations_manager.recommendation_models.recommender_model import (
    RecommenderModel,
)


class RecommenderManager:
    def __init__(self):
        self.models: Dict[str, RecommenderModel] = {
            "Moodika-Model-A": MoodikaAAdapter(
                {
                    "name": "Moodika-Model-A",
                    "description": "A playlist-based model that averages results from user-created Spotify playlists to provide recommendations. It leverages the collective input from existing playlists to generate a song profile.",
                    "version": "1.0",
                },
            ),
            "ChatGPT": ChatGPTAdapter(
                {
                    "name": "ChatGPT",
                    "description": "Utilizes ChatGPT to derive Spotify parameters for generating recommendations, offering a conversational interface for personalized music suggestions.",
                    "version": "3.0",
                },
            ),
        }

    def add_model(self, model: RecommenderModel):
        self.models[model.name] = model

    def get_all_models(self) -> List[RecommenderModel]:
        return list(self.models.values())

    def get_model_by_name(self, name: str) -> RecommenderModel:
        return self.models.get(name)

    def generate_playlist(
        self,
        prompt: str,
        config: dict,
        context: dict,
        access_token: str,
    ) -> dict:
        model = self.get_model_by_name(config.get("model"))
        if not model:
            requested_model = config.get("model")
            raise ValueError(f"Model {requested_model} not found")
        model.initialize(access_token=access_token)
        response = model.generate_playlist(prompt, config, context)
        model.finalize()
        return response
