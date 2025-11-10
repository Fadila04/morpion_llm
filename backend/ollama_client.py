import requests
import json

def get_model(grid, active_player, model_name="llama3.2:1b"):
    """
    Cette fonction envoie la grille et le joueur actif au modèle Ollama
    et récupère la position du coup que le modèle propose."""

    # Transformation de la grille en texte
    grid_text = "\n".join([" | ".join(cell or " " for cell in row) for row in grid])

    # Création du prompt
    prompt = f"""
You are a Tic-Tac-Toe expert. 
Game rules:
- Two players alternate placing marks: 'X' and 'O'.
- The board is 10x10 (rows and columns indexed 0..9).
- The goal is to align 5 of your marks horizontally, vertically, or diagonally.
- You MUST NOT place a mark on an occupied cell.
Task:
Given the current board and the active player, choose the single best move following this priority:
 1) If you can win immediately with one move, play that winning move.
 2) Else if the opponent can win on their next move, play the blocking move.
 3) Else play the most strategic move (center, extend your lines).

Input format:
The board is shown as lines with characters 'X', 'O', or '.' for empty.

Here is the current grid:
{grid_text}

player: {active_player}
Respond **only** in JSON format like this:
{{
  "row": <row_index>,
  "col": <col_index>
}}
For example:
{{
  "row": 1,
  "col": 2
}}
Do not add any explanation or text, just the JSON.
    """

# appel API locale Ollama
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model_name, "prompt": prompt, "stream": False},
            timeout=180
        )
        response.raise_for_status()    # Vérifie si l'appel à reussie
    

        # Lecture de la réponse du modéle
        data = response.json()
        text_output = data.get("response", "").strip()

        print(f"Réponse brute du modèle : {text_output}")

        # réponse attendu
        try:
            move = json.loads(text_output)
            row = move.get("row") 
            col = move.get("col")
            if row is not None and col is not None:
                return {"row":int(row), "col": int(col)}
        except json.JSONDecodeError:
            print(f" Réponse du modéle nonJSON : {text_output}")
            return None
    
    except Exception as e:
        print(f" Erreur lors de l'appel au modéle: {e}")
        return None


    





    
