from pydantic import BaseModel
from typing import List, Literal, Optional # <-- Ajout de Optional et Literal

# format de données (schéma JSON que le front doit envoyer à l'API)
class PlayRequest(BaseModel):
    grid: List[List[str]]  # La grille 10x10 : "", "X", "O"
    active_player: Literal["X", "O"] # Le joueur actif
    model_name: str  # Le model ollama

class Move(BaseModel):
    row: int
    col: int

# format de réponse JSON
class PlayResponse(BaseModel):
    grid: List[List[str]]
    # move est Optionnel car il est None en cas de "draw"
    move: Optional[Move] 
    status: Literal["continue", "win", "draw"]   
    # player est Optionnel car il est None en cas de "draw"
    player: Optional[Literal["X", "O"]] 
    message: Optional[str] = None







