from abc import ABC, abstractmethod


class RecommenderModel(ABC):
    def __init__(self, model_config: dict):
        """
        Initialize the RecommenderModel with the given configuration.

        Args:
            config (dict): Configuration dictionary containing model name, description, and version.
        """
        self.name = model_config.get("name")
        self.description = model_config.get("description")
        self.version = model_config.get("version")

    def get_model_info(self):
        """
        Get information about the model.

        Returns:
            dict: Dictionary containing model name, description, and version.
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
        }

    @abstractmethod
    def generate_playlist(self, prompt, config, context):
        """
        Generate a playlist based on the provided prompt, configuration, and context.
        This method should be implemented by subclasses.

        Args:
            prompt (str): The input prompt for generating recommendations.
            config (dict): Additional configuration for the recommendation.
            context (dict): Contextual information for generating recommendations.
        """

    @abstractmethod
    def initialize(self):
        """
        Initialize the model. This method should be implemented by subclasses.
        """

    @abstractmethod
    def finalize(self):
        """
        Finalize the model. This method should be implemented by subclasses for cleanup operations.
        """
