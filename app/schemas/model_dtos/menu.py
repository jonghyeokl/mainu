from pydantic import BaseModel

from app.db.models.menu.menu import Menu


class MenuModelDTO(BaseModel):
    menu_id: str
    name: str

    @classmethod
    def from_model(cls, model: Menu) -> "MenuModelDTO":
        return cls(
            menu_id=str(model.menu_id),
            name=model.name,
        )
