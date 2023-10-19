from src.enums import Permission
from pydantic import BaseModel


class CreateUserRequestDTO(BaseModel):
    email: str
    position: str | None
    permissions: list[Permission]


class ChangeUserRequestDTO(BaseModel):
    email: str
    position: str | None
    permissions: list[Permission]
