from typing import Any, Dict, List

from pydantic import BaseModel
from pydantic import Field

from app.schemas.dtos.recommend import ChoiceCreateRequestDTO


class SelectRequestBody(BaseModel):
    user_id: str = Field(..., description="User ID")
    text: str = Field(..., description="Original natural language input")
    menu_id: str = Field(..., description="Selected menu ID (UUID)")
    parsed_features: List[Dict[str, Any]] = Field(..., description="Parsed features from LLM")

    def to_choice_create_request_dto(self) -> ChoiceCreateRequestDTO:
        return ChoiceCreateRequestDTO(
            user_id=self.user_id,
            text=self.text,
            parsed_features=self.parsed_features,
            selected_menu_id=self.menu_id,
        )
