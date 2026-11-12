from pydantic import BaseModel

class AgriculturalResourceBase(BaseModel):
    culture: str
    calendrier: dict | None = None
    rendement: str | None = None
    conseils: str | None = None

class AgriculturalResourceOut(AgriculturalResourceBase):
    id: int

    class Config:
        from_attributes = True
