from pydantic import BaseModel

class Arena(BaseModel):
    number: int # Numéro de l'arène
    name: str   # Nom de l'arène
    image: str  # URL de l’image
    min_trophies: int
