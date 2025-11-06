import requests
import json

def get_model(grid, active_player, model_name="llama2"):
    """
    Cette fonction envoie la grille et le joueur actif au modèle Ollama
    et récupère la position du coup que le modèle propose."""

    # Transformation de la grille en texte
    grid_text = "\n".join([" | ".join(cell or " " for cell in row) for row in grid])

    # Création du prompt
    prompt = f"""
You are a Tic-Tac-Toe player. 
In Tic-Tac-Toe, two players take turns placing their marks (an 'x' for player 'x' and an 'o' for player 'o') 
on a 10X10 grid. The goal is to get 5 of your marks in a row, either horizontally, vertically, or diagonally. 
If all spaces on the grid are filled and neither player has achieved three in a row, the game ends in a draw.

Here is the current grid (empty spaces are shown as blanks):

{grid_text}

It is now player '{active_player}'’s turn. 
Please respond **only** in JSON format like this:
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
            timeout=60
        )
        response.raise_for_status()    # Vérifie si l'appel à reussie
    

        # Lecture de la réponse du modéle
        data = response.json()
        text_output = data.get("response", "").strip()

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


    





    
