from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.menu.menu import Menu
from app.schemas.model_dtos.menu import MenuModelDTO


class MenuRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @classmethod
    def build(
        cls,
        db: AsyncSession = Depends(get_db),
    ) -> "MenuRepository":
        return cls(db=db)

    async def get_all(self) -> List[MenuModelDTO]:
        query = await self.db.execute(select(Menu))
        menus = query.scalars().all()
        return [MenuModelDTO.from_model(m) for m in menus]

    async def find_by_id(self, menu_id: int) -> Optional[MenuModelDTO]:
        query = await self.db.execute(select(Menu).where(Menu.id == menu_id))
        menu = query.scalars().one_or_none()
        return MenuModelDTO.from_model(menu) if menu else None
