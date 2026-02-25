from pydantic import BaseModel
from pydantic import Field

from app.schemas.dtos.recommend import RecommendRequestDTO


class RecommendRequestBody(BaseModel):
    user_id: str = Field(..., description="User ID")
    text: str = Field(..., description="Natural language input from user")

    def to_recommend_request_dto(self) -> RecommendRequestDTO:
        return RecommendRequestDTO(
            user_id=self.user_id,
            text=self.text,
        )
