from pydantic import BaseModel

from app.db.models.menu.menu import Menu


class MenuModelDTO(BaseModel):
    id: str
    name: str

    @classmethod
    def from_model(cls, model: Menu) -> "MenuModelDTO":
        return cls(
            id=str(model.id),
            name=model.name,
        )
