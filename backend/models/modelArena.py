from pydantic import BaseModel

class Arena(BaseModel):
    number: int
    name: str
    image: str  # URL de l’image
    min_trophies: int
