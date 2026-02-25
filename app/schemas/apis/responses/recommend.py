from typing import Any, Dict, List

from pydantic import BaseModel

from app.schemas.model_dtos.menu import MenuModelDTO


class RecommendResponse(BaseModel):
    parsed_features: List[Dict[str, Any]]
    recommended_menus: List[MenuModelDTO]
