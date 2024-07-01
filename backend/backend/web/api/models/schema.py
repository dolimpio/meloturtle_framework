from pydantic import BaseModel


class RecommendationModel(BaseModel):
    """Model for returning recommendation models."""

    name: str
    description: str
    version: str
