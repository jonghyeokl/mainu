from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from app.schemas.apis.requests.recommend import RecommendRequestBody
from app.schemas.apis.responses.recommend import RecommendResponse
from app.services.jwt import JwtService
from app.services.recommend import RecommendService
from app.utils.jwt_bearer import get_access_token

router = APIRouter()


@router.post(
    "/",
    response_model=RecommendResponse,
)
async def recommend(
    access_token: Annotated[str, Depends(get_access_token)],
    request_body: RecommendRequestBody,
    recommend_service: RecommendService = Depends(RecommendService.build),
) -> RecommendResponse:
    JwtService().validate_access_token(access_token)
    return await recommend_service.recommend(request_body.to_recommend_request_dto())
