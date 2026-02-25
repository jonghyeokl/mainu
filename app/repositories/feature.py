from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.feature.feature import Feature
from app.schemas.model_dtos.feature import FeatureModelDTO


class FeatureRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @classmethod
    def build(
        cls,
        db: AsyncSession = Depends(get_db),
    ) -> "FeatureRepository":
        return cls(db=db)

    async def get_all(self) -> List[FeatureModelDTO]:
        query = await self.db.execute(select(Feature))
        features = query.scalars().all()
        return [FeatureModelDTO.from_model(f) for f in features]
