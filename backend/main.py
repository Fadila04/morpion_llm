from fastapi import FastAPI
from backend.ollama_client import get_llm_model
from backend.game_logic import check_winner
from backend.schemas import PlayRequest, PlayResponse

app = FastAPI()

#  Route test simple
@app.get("/")
def ping():
    return {"message": "Bienvenue sur l'API Morpion", "status": "OK"}


# Route principale : fait jouer le modèle reçu
@app.post("/play")
def play(request: PlayRequest):
    """
    Cette route reçoit :
      - la grille actuelle,
      - le joueur actif ('X' ou 'O'),
      - et le nom du modèle à utiliser.
    Elle renvoie la grille mise à jour + le statut du jeu.
    """

    grid = request.grid
    active_player = request.active_player
    model_name = request.model_name

    # Vérifie les cases encore libres 
    grid_size = len(grid)
    empty_cells = [(r, c) for r in range(grid_size) for c in range(grid_size) if grid[r][c] == ""]
    if not empty_cells:
        return PlayResponse(grid=grid, move={}, status="draw", message="Match nul !")

    #  Appel du modèle (Ollama ou Azure) 
    move = get_llm_model(grid, active_player, model_name)
    if not move:
        return PlayResponse(grid=grid, move={}, status="error", message="Aucun coup renvoyé par le modèle.")

    row_move, col_move = move["row"], move["col"]

    #  Joue le coup 
    new_grid = [row_.copy() for row_ in grid]
    new_grid[row_move][col_move] = active_player

    #  Vérifie si ce coup fait gagner le joueur 
    if check_winner(new_grid, active_player):
        return PlayResponse(
            grid=new_grid,
            move={"row": row_move, "col": col_move},
            status="win",
            player=active_player,
            message=f"Le joueur {active_player} ({model_name}) a gagné !"
        )
    # --- Sinon, prépare la suite du tour ---
    next_player = "O" if active_player == "X" else "X"
    next_model = "o4-mini" if model_name != "o4-mini" else "llama3.2:1b"

    return PlayResponse(
        grid=new_grid,
        move={"row": row_move, "col": col_move},
        status="continue",
        player=next_player,
        message=f"Prochain tour : {next_player} ({next_model})"
    )
