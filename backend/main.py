from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from backend.ollama_client import get_llm_model
from backend.game_logic import check_winner
from backend.schemas import PlayRequest, PlayResponse, Move # <-- IMPORT DE MOVE
from fastapi.middleware.cors import CORSMiddleware # <-- NOUVEL IMPORT

app = FastAPI()

# --- Configuration CORS (Obligatoire) ---
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)
# ----------------------------------------

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
            move=None, # <-- CORRECTION : None au lieu de {}
            status="draw",
            message="Match nul !",
            player=None # Nouveau champ
        )

    # Appel du modéle ollama pour obtenir le coup
    move_data = get_llm_model(request.grid, request.active_player, request.model_name)
    row_move, col_move = move_data["row"], move_data["col"]

    # Mise à jour de la grille localement
    new_grid = [row_.copy() for row_ in request.grid]
    new_grid[row_move][col_move] = request.active_player

    # Vérifie si le joueur a gagné après un coup
    if check_winner(new_grid, request.active_player):
        return PlayResponse(
            grid=new_grid,
            move=Move(row=row_move, col=col_move), # Utiliser le Pydantic Model Move
            status="win",
            player=request.active_player
        )
    else:
        # Renvoie de la réponse sous JSON
        next_player = "O" if request.active_player == "X" else "X" # <-- DÉTERMINER JOUEUR SUIVANT
        return PlayResponse(
            grid=new_grid,
            move=Move(row=row_move, col=col_move), # Utiliser le Pydantic Model Move
            status="continue",
            player=next_player # <-- CORRECTION : Passer au joueur suivant
        )