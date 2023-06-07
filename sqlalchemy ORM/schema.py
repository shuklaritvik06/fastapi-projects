from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str


class ItemSchema(BaseModel):
    title: str
    description: str
    owner_id: int
