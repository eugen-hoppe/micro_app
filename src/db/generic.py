from pydantic import BaseModel


class Data(BaseModel):
    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


class Shape(BaseModel):
    id: int
    alias: str
    data: dict
    version: int

    class Config:
        from_attributes = True

    @classmethod
    def from_db(cls, row):
        return cls(**row.__dict__)


class Update(BaseModel):
    id: int | None = None
    alias: str | None = None
    data: dict | None = None

    class Config:
        from_attributes = True
