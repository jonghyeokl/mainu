import datetime
import uuid
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models.choice.choice import Choice
from app.schemas.model_dtos.choice import ChoiceModelDTO
from app.schemas.dtos.recommend import ChoiceCreateRequestDTO


class ChoiceRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @classmethod
    def build(
        cls,
        db: AsyncSession = Depends(get_db),
    ) -> "ChoiceRepository":
        return cls(db=db)

    async def create(self, dto: ChoiceCreateRequestDTO) -> ChoiceModelDTO:
        now = datetime.datetime.utcnow()
        new_choice = Choice(
            id=uuid.uuid4(),
            user_id=UUID(dto.user_id),
            text=dto.text,
            parsed_features=dto.parsed_features,
            selected_menu_id=UUID(dto.selected_menu_id),
            created_dt=now,
            updated_dt=now,
        )
        self.db.add(new_choice)
        await self.db.commit()
        return ChoiceModelDTO.from_model(new_choice)
