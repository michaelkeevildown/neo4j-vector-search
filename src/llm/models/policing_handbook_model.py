from pydantic import BaseModel, Field

class PolicingHandbookModel(BaseModel):
    summary: str = Field(
        description="Provide a one-sentence summary of the current text.")
    topics: list = Field(
        description="Provide a list of topics that are discussed. Score each topic by its relevance in current text: [{'id': 'single-car-policy', 'description': 'Single Car Policy','relevance_score': 0.85}, {'id': 'multicover-car-policy', 'description': 'MultiCover Policy','relevance_score': 0.15}]")
