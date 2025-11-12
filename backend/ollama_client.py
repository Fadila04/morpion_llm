import os
import ast
import requests
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

# Chargement des variables d'environnement
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

def get_llm_model(grid, active_player, model_name="llama3.2:1b"):
    """
    Gère à la fois Ollama (local) et Azure OpenAI pour générer un coup de morpion.
    Retourne un dictionnaire {"row": x, "col": y}.
    """

    # Transformation de la grille en texte
    grid_text = "\n".join([" | ".join(cell or "." for cell in row) for row in grid])

    prompt = f"""
    You are a Tic-Tac-Toe expert. 
Game rules:
- Two players alternate placing marks: 'X' and 'O'.
- The board is 10x10 (rows and columns indexed from 0 to 9).
- The goal is to align 5 of your marks horizontally, vertically, or diagonally.
- You MUST NOT place a mark on an occupied cell.

Task:
Given the current board and the active player, choose the single best move following this priority:
1. Check if the cell is EMPTY (contains '.')
2. If you can WIN immediately with one move → play that winning move
3. Else if opponent can WIN on their next move → BLOCK that move
4. Else play strategically (center area, extend your lines, create threats)
5. If your chosen cell is occupied → restart from step 1 with another cell

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
  "row": 4,
  "col": 7
}}

Do not add any explanation or text, just the JSON.
    """

    # --- Cas Azure OpenAI ---
    if model_name == "o4-mini":
        try:
            client = AzureOpenAI(
                api_key=os.getenv("AZURE_API_KEY"),
                api_version="2024-12-01-preview",
                azure_endpoint=os.getenv("AZURE_ENDPOINT")
            )

            response = client.chat.completions.create(
                model=os.getenv("AZURE_MODEL", "o4-mini"),
                messages=[
                    {"role": "system", "content": "Tu es un joueur de morpion stratégique."},
                    {"role": "user", "content": prompt}
                ]
            )

            move_text = response.choices[0].message.content.strip()
            print("Réponse brute Azure :", move_text)

            # Essaye de convertir la réponse en dictionnaire Python
            move = json.loads(move_text)
            row = move.get("row")
            col = move.get("col")

            if row is not None and col is not None:
                return {"row": int(row), "col": int(col)}
        except Exception as e:
            print("Erreur Azure :", e)
            return None

    # --- Cas Ollama local ---
    else:
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()

            data = response.json()
            text_output = data.get("response", "").strip()
            print("Réponse brute Ollama :", text_output)

            # Décoder la sortie JSON
            try:
                move = json.loads(text_output)
                row = move.get("row")
                col = move.get("col")

                if row is not None and col is not None:
                    return {"row": int(row), "col": int(col)}
            except json.JSONDecodeError:
                print(f"Réponse du modèle non JSON : {text_output}")
                return None
            
        except Exception as e:
            print(f"Erreur lors de l'appel au modèle Ollama : {e}")
            return None



























    





    
    





    
