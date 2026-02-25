from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class RecommendRequestDTO:
    user_id: str
    text: str


@dataclass
class ParsedFeatureDTO:
    feature_id: str
    value: str


@dataclass
class ChoiceCreateRequestDTO:
    user_id: str
    text: str
    parsed_features: List[Dict[str, Any]]
    selected_menu_id: str
