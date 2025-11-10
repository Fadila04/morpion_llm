import requests
import json

url = "http://127.0.0.1:8000/play"

#  Cas : partie en cours
grid_continue = [[""] * 10 for _ in range(10)]
grid_continue[0][0] = "X"
grid_continue[0][1] = "O"

# Cas : victoire (simulateur)
grid_win = [[""] * 10 for _ in range(10)]
for i in range(4):
    grid_win[0][i] = "X" 
# Le modèle doit logiquement jouer en (0,4) pour gagner

#  match nul (grille pleine)
grid_draw = [["X" if (i + j) % 2 == 0 else "O" for j in range(10)] for i in range(10)]

#  Création des requêtes
tests = [
    ("continue", grid_continue),
    ("win", grid_win),
    ("draw", grid_draw),
]

for test_name, grid in tests:
    print(f"\n=== Test scénario : {test_name.upper()} ===")
    payload = {
        "grid": grid,
        "active_player": "X",
        "model_name": "llama3.2:1b"
    }

    response = requests.post(url, json=payload)

    print("Statut HTTP :", response.status_code)
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception:
        print("Erreur de parsing JSON :", response.text)










