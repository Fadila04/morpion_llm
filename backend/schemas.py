from pydantic import BaseModel
from typing import List


# format de données (schéma JSON que le front doit envoyé à l'API)
class PlayRequest(BaseModel):
    grid: List[List[str]]  # La grille
    active_player: str  # "X" ou "O"
    model_name: str  # Le model ollama


# format de réponse JSON
class PlayResponse(BaseModel):
    grid: List[List[str]]
    move: dict
    status: str   # "Continue","win" or "draw"


