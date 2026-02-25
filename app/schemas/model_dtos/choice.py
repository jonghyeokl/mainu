from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel

from app.db.models.choice.choice import Choice


class ChoiceModelDTO(BaseModel):
    id: str
    user_id: str
    text: str
    parsed_features: List[Dict[str, Any]]
    selected_menu_id: str
    created_dt: datetime
    updated_dt: datetime

    @classmethod
    def from_model(cls, model: Choice) -> "ChoiceModelDTO":
        return cls(
            id=str(model.id),
            user_id=str(model.user_id),
            text=model.text,
            parsed_features=model.parsed_features,
            selected_menu_id=str(model.selected_menu_id),
            created_dt=model.created_dt,
            updated_dt=model.updated_dt,
        )
