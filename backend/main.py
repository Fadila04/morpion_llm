from fastapi import FastAPI
from backend.ollama_client import get_llm_model
from backend.game_logic import check_winner
from backend.schemas import PlayRequest, PlayResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (tu peux restreindre ensuite)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers (Content-Type, etc.)
)

#  Route test simple
@app.get("/")
def ping():
    return {"message": "Bienvenue sur l'API Morpion", "status": "OK"}


# Route principale : fait jouer le modèle reçu
@app.post("/play")
def play(request: PlayRequest):
    print("\n=== Nouvelle requête reçue ===")
    print("Grille reçue :", request.grid)
    print("Joueur actif :", request.active_player)
    print("Modèle :", request.model_name)

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
    print(f'Cout jouer par {active_player} {move}')
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

    # Fait jouer le second modèle
    move2 = get_llm_model(grid, next_player, next_model)
    if move2:
        r2, c2 = move2["row"], move2["col"]
        if 0 <= r2 < len(grid) and 0 <= c2 < len(grid) and grid[r2][c2] == "":
            grid[r2][c2] = next_player
            if check_winner(grid, next_player):
                return PlayResponse(grid=grid, move={"row": r2, "col": c2}, status="win")

    return PlayResponse(
        grid=new_grid,
        move={"row": row_move, "col": col_move},
        status="continue",
        player=next_player,
        message=f"Prochain tour : {next_player} ({next_model})"
    )
