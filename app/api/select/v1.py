from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from app.schemas.apis.requests.select import SelectRequestBody
from app.schemas.model_dtos.choice import ChoiceModelDTO
from app.services.jwt import JwtService
from app.services.recommend import RecommendService
from app.utils.jwt_bearer import get_access_token

router = APIRouter()


@router.post(
    "/",
    response_model=ChoiceModelDTO,
)
async def select_menu(
    access_token: Annotated[str, Depends(get_access_token)],
    request_body: SelectRequestBody,
    recommend_service: RecommendService = Depends(RecommendService.build),
) -> ChoiceModelDTO:
    JwtService().validate_access_token(access_token)
    return await recommend_service.save_choice(request_body.to_choice_create_request_dto())
