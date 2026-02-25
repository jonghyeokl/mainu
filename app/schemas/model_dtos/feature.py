from typing import List

from pydantic import BaseModel

from app.db.models.feature.feature import Feature


class FeatureModelDTO(BaseModel):
    feature_id: str
    feature: str
    available_values: List[str]

    @classmethod
    def from_model(cls, model: Feature) -> "FeatureModelDTO":
        return cls(
            feature_id=str(model.feature_id),
            feature=model.feature,
            available_values=model.available_values,
        )
