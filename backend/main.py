from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from backend.ollama_client import get_model
from backend.game_logic import check_winner

app = FastAPI()

# format de données (schéma JSON que le front doit envoyé à l'API)
class PlayRequest(BaseModel):
    grid: List[List[str]]  # La grille
    active_player: str  # "X" ou "Y"
    model_name: str  # Le model ollama

# format de réponse JSON
class PlayResponse(BaseModel):
    grid: List[List[str]]
    move: dict
    status: str   # "Continue","win" or "draw"

# Route test
@app.get("/")
def ping():
    return{"message": "Bienvenue sur API Morpion", "status": "OK"}

# Route principale
@app.post("/play")
def play(request: PlayRequest):

    """Cette route reçoit la demande sous format(PlayRequest) 
    et renvoie le PlayResponse """

    # Récupération des cases vides
    grid_size = len(request.grid)
    empty_grids = [(r, c) for r in range(grid_size) for c in range(grid_size) if request.grid[r][c] == ""]

    # Conditions si match nul
    if not empty_grids:
        return PlayResponse(
            grid= request.grid,
            move={},
            status="draw"
        )
    # Appel du modéle ollama pour obtenir le coup
    move= get_model(request.grid, request.active_player, request.model_name)
    row, col = move["row"], move["col"]

    # Mise à jour de la grille localement
    new_grid = [row.copy() for row in request.grid]
    new_grid[row][col] = request.active_player

    #  Vérifie si le joueuer à gagné aprés un coup
    if check_winner(new_grid, request.active_player):
        return PlayResponse(
            grid=new_grid,
            move={"row":row, "col": col},
            status="win"
        )

    # Renvoie de la réponse sous JSON
    return PlayResponse(
        grid=new_grid,
        move={"row":row, "col": col},
        status="continue"
    )


