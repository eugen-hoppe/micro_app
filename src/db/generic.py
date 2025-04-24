from pydantic import BaseModel


class Data(BaseModel):
    def db(self) -> dict:
        return self.model_dump(exclude_none=True)


class Shape(BaseModel):
    id: int
    alias: str
    data: dict
    version: int

    class Config:
        from_attributes = True


class Update(BaseModel):
    id: int | None = None
    alias: str
    data: dict | None = None

    class Config:
        from_attributes = True
