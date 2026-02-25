import json
import os
from typing import Any, Dict, List

import requests
from fastapi import Depends, HTTPException

from app.repositories.feature import FeatureRepository
from app.repositories.menu import MenuRepository
from app.repositories.choice import ChoiceRepository
from app.schemas.model_dtos.feature import FeatureModelDTO
from app.schemas.model_dtos.menu import MenuModelDTO
from app.schemas.model_dtos.choice import ChoiceModelDTO
from app.schemas.dtos.recommend import RecommendRequestDTO, ChoiceCreateRequestDTO
from app.schemas.apis.responses.recommend import RecommendResponse


class RecommendService:
    def __init__(
        self,
        feature_repository: FeatureRepository,
        menu_repository: MenuRepository,
        choice_repository: ChoiceRepository,
    ) -> None:
        self.feature_repository = feature_repository
        self.menu_repository = menu_repository
        self.choice_repository = choice_repository

    @classmethod
    def build(
        cls,
        feature_repository: FeatureRepository = Depends(FeatureRepository.build),
        menu_repository: MenuRepository = Depends(MenuRepository.build),
        choice_repository: ChoiceRepository = Depends(ChoiceRepository.build),
    ) -> "RecommendService":
        return cls(
            feature_repository=feature_repository,
            menu_repository=menu_repository,
            choice_repository=choice_repository,
        )

    async def recommend(self, dto: RecommendRequestDTO) -> RecommendResponse:
        features = await self.feature_repository.get_all()
        menus = await self.menu_repository.get_all()

        parsed_features = await self.extract_features(dto.text, features)
        recommended_menus = await self.recommend_menus(parsed_features, menus)

        return RecommendResponse(
            parsed_features=parsed_features,
            recommended_menus=recommended_menus,
        )

    async def save_choice(self, dto: ChoiceCreateRequestDTO) -> ChoiceModelDTO:
        return await self.choice_repository.create(dto)

    async def extract_features(
        self,
        text: str,
        features: List[FeatureModelDTO],
    ) -> List[Dict[str, Any]]:
        allowed_features = [
            {
                "feature_id": f.feature_id,
                "feature": f.feature,
                "available_values": f.available_values,
            }
            for f in features
        ]

        prompt = f"""아래 문장을 분석하여 ALLOWED_FEATURES에 정의된 값 중에서만 선택해 JSON 배열로 반환해.
반드시 다음 형식으로만 출력해: [{{"id": <feature_id>, "value": "<value>"}}]
다른 텍스트나 설명은 절대 포함하지 마. 오직 JSON 배열만 출력해.
해당 없는 feature는 포함하지 마.

ALLOWED_FEATURES:
{json.dumps(allowed_features, ensure_ascii=False)}

분석할 문장: {text}"""

        response_text = await self._call_gemini(prompt)

        try:
            start = response_text.find("[")
            end = response_text.rfind("]") + 1
            parsed = json.loads(response_text[start:end])
            return parsed
        except (json.JSONDecodeError, ValueError):
            return []

    async def recommend_menus(
        self,
        parsed_features: List[Dict[str, Any]],
        menus: List[MenuModelDTO],
    ) -> List[MenuModelDTO]:
        menu_list = [{"id": m.id, "name": m.name} for m in menus]

        prompt = f"""아래 사용자 선호 features를 바탕으로 MENU_LIST에서 가장 잘 맞는 메뉴 상위 5개를 추천해.
반드시 다음 형식으로만 출력해: [{{"id": <menu_id>, "name": "<menu_name>"}}]
다른 텍스트나 설명은 절대 포함하지 마. 오직 JSON 배열만 출력해.
MENU_LIST에 없는 메뉴는 절대 포함하지 마.

USER_FEATURES:
{json.dumps(parsed_features, ensure_ascii=False)}

MENU_LIST:
{json.dumps(menu_list, ensure_ascii=False)}"""

        response_text = await self._call_gemini(prompt)

        try:
            start = response_text.find("[")
            end = response_text.rfind("]") + 1
            parsed = json.loads(response_text[start:end])
            menu_map = {m.id: m for m in menus}
            result = []
            for item in parsed:
                menu_id = item.get("id")
                if menu_id in menu_map:
                    result.append(menu_map[menu_id])
            return result
        except (json.JSONDecodeError, ValueError):
            return []

    async def _call_gemini(self, prompt: str) -> str:
        API_KEY = os.getenv("GENAI_API_KEY")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 1000,
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            print(response.text)
            raise HTTPException(status_code=response.status_code, detail="genai api error")

        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
