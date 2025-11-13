# morpion_llm

Pour lancer l'app API : uvicorn backend.main:app --reload
"stream": False ( Permet de récuperer lechoix final du modéle et ne pas avoir tous la reflexion de réponse du modéle)


🧠 Morpion IA — Duel entre un humain et un modèle LLM (Ollama)

# Description du projet
Ce projet consiste à développer un jeu de Morpion (Tic Tac Toe) où un modèle d’intelligence artificielle (LLM) joue automatiquement contre l’utilisateur.
Le backend est construit avec FastAPI, et l’IA utilise un modèle local via Ollama (ici llama3.2:1b) pour choisir les coups à jouer.
Le frontend en HTML / CSS / JavaScript permet d’interagir avec le jeu via une grille interactive et un bouton Play.


# Fonctionnalités principales :
Interface graphique simple et interactive (HTML / CSS / JS)
API REST avec FastAPI
Intégration d’un modèle LLM Ollama pour jouer automatiquement
Gestion du plateau et des règles du jeu (détection du gagnant, tour de jeu, etc.)
Communication sécurisée entre le frontend et le backend (CORS activé)

# ARCHITECTURE:
morpion_llm/
│
├── .venv
├── backend/
│   ├── main.py                # Point d’entrée FastAPI
│   ├── game_logic.py          # Gestion du plateau et de la logique du jeu
│   ├── model_ollama.py        # Communication avec le modèle Ollama
    ├── schemas.py             # Création des classes de l'API
    ├── test_api.py            # Pour réaliser les tests avant la construiction de l'interface
│   └── __init__.py
│
├── frontend/
│   ├── index.html             # Interface utilisateur
│   ├── script.js              # Logique du jeu côté client
│   ├── style.css              # Apparence du jeu
│

├── Dockerfile
├── .dockerignore
├── .env
├── requirements.txt
└── README.md



# Lancer le backend main.api
- Pour démarrer le serveur depuis le fichier backend : uvicorn main:app --reload

# Lancer le front end
ouvrir le fichier : frontend/index.html
- dans votre navigateur (double-clic ou via un serveur local).
- Le bouton "Play" permet de démarrer la partie.
- Le joueur humain joue en X, et le modèle IA joue en O.


# Technologie utiliser
| Domaine       | Outils                |
| ------------- | --------------------- |
| Backend       | FastAPI               |
| IA locale     | o4.mini + Llama3.2    |
| Frontend      | HTML, CSS, JavaScript |
| Serveur       | Uvicorn               |
| Environnement | Python 3.12+          |


# Deploiment
Faire un deploiment avec docker sur le serveur Azure

# AUTEUR
Fadilatou OUMAROU et Emese HOFFMAN


# DIAGRAMME CHRONOLOGIQUE

CLICK SUR JOUER
    |
    |
    ↓

Active_player = X(Ollama)
    |
    |
    ↓

Appel API Fast API (Le modéle joue un coup)
    |
    |
    ↓

Backend Renvoie nouvelle grille + état (win, continue, draw)
    |
    |
    ↓

Affichage de grille mise à jour
    |
    |
    ↓

Change de joueuer et relance le tour
