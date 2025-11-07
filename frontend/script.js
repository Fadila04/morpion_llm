/* ============================================================================
 *  script.js — Front minimal pour piloter l'API FastAPI /play
 *  ----------------------------------------------------------------------------
 *  - Gère l'état local de la grille (10×10 de chaînes "", "X" ou "O")
 *  - Rendu de la grille en <table> avec en-têtes A–J et 1–10
 *  - Appel du backend: POST /play avec { grid, active_player, model_name }
 *  - Mise à jour du plateau et affichage du statut
 * ========================================================================== */

/**
 * Crée une grille 10×10 initialisée avec des chaînes vides "" (cases libres).
 * @param {number} size - Taille de la grille (par défaut 10).
 * @returns {string[][]} - Tableau 2D de strings.
 */
function makeEmptyGrid(size = 10) {
return Array.from({ length: size }, () => Array(size).fill(""));
}

/**
 * Récupère une référence unique d'éléments DOM nécessaires.
 * L'idée est d'éviter des getElementById répétés et centraliser les ids.
 */
const DOM = {
board: document.getElementById("board"),
status: document.getElementById("status"),
log: document.getElementById("log"),
modelName: document.getElementById("modelName"),
activePlayer: document.getElementById("activePlayer"),
btnPlay: document.getElementById("btnPlay"),
btnReset: document.getElementById("btnReset"),
};

/**
 * État applicatif minimal du front.
 * - grid: grille 10×10 (strings "", "X", "O")
 * - size: dimension (10)
 */
const state = {
size: 10,
grid: makeEmptyGrid(10),
};

/**
 * Affiche un message d'état (ok/erreur) dans la barre de statut.
 * @param {string} msg - Message à afficher.
 * @param {"ok"|"err"|""} level - Niveau d'importance (couleur).
 */
function setStatus(msg, level = "") {
DOM.status.className = `status ${level}`;
DOM.status.textContent = msg;
}

/**
 * Ajoute une entrée dans le petit journal en bas de page.
 * @param {any} entry - Valeur loggable (string ou objet).
 */
function log(entry) {
const text = typeof entry === "string" ? entry : JSON.stringify(entry, null, 2);
DOM.log.textContent = `${text}\n${DOM.log.textContent}`;
}

/**
 * Construit l'en-tête (A–J) et les lignes (1–10) + cellules dans la <table>.
 * On sépare la génération du DOM du "state" pour clarifier la logique.
 */
function buildBoardSkeleton() {
  // Efface la table
DOM.board.innerHTML = "";

const size = state.size;
const thead = document.createElement("thead");
const thr = document.createElement("tr");

  // Première cellule vide (coin supérieur gauche)
const corner = document.createElement("th");
thr.appendChild(corner);

  // En-têtes de colonnes A, B, C... J
for (let c = 0; c < size; c++) {
    const th = document.createElement("th");
    th.textContent = String.fromCharCode(65 + c); // 65 = 'A'
    thr.appendChild(th);
}
thead.appendChild(thr);
DOM.board.appendChild(thead);

  // Corps du tableau
const tbody = document.createElement("tbody");

for (let r = 0; r < size; r++) {
    const tr = document.createElement("tr");

    // En-tête de ligne (1..10)
    const thRow = document.createElement("th");
    thRow.textContent = String(r + 1);
    tr.appendChild(thRow);

    // Cellules
    for (let c = 0; c < size; c++) {
    const td = document.createElement("td");
    td.dataset.row = String(r);
    td.dataset.col = String(c);
    tr.appendChild(td);
    }

    tbody.appendChild(tr);
}

DOM.board.appendChild(tbody);
}

/**
 * Met à jour le contenu visuel de chaque cellule à partir de state.grid.
 * On ne rend pas cliquable (le LLM joue). Tu peux ajouter un onClick si besoin.
 */
function renderBoardValues() {
  const cells = DOM.board.querySelectorAll("td");
  cells.forEach((td) => {
    const r = Number(td.dataset.row);
    const c = Number(td.dataset.col);
    td.textContent = state.grid[r][c] || "";
  });
}

/**
 * Envoie une requête POST au backend /play pour demander le prochain coup au LLM.
 * @returns {Promise<void>}
 */
async function playTurn() {
const payload = {
    grid: state.grid,
    active_player: DOM.activePlayer.value, // "X" ou "O"
    model_name: DOM.modelName.value || "llama3:8b",
};

setStatus("Requête en cours…");
const t0 = performance.now();

try {
    const res = await fetch("/play", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    });

    const txt = await res.text();
    // Essaye de parser JSON quoi qu’il arrive (utile pour logs de debug)
    let out;
    try {
    out = JSON.parse(txt);
    } catch {
    throw new Error(`Réponse non-JSON: ${txt}`);
    }

    if (!res.ok) {
    throw new Error(out?.detail || res.statusText);
    }

    // out = { grid, move: {row,col}, status }
    state.grid = out.grid;
    renderBoardValues();

    const dt = Math.round(performance.now() - t0);
    setStatus(`Coup joué en ${dt} ms — statut: ${out.status}`, "ok");
    log({ request: payload, response: out });

    // Si la partie continue, alterne le joueur côté UI (optionnel)
    if (out.status === "continue") {
    const next = DOM.activePlayer.value === "X" ? "O" : "X";
    DOM.activePlayer.value = next;
    }
} catch (err) {
    console.error(err);
    setStatus(`Erreur: ${err.message}`, "err");
    log(String(err));
}
}

/**
 * Réinitialise la grille côté front uniquement.
 * (Si tu ajoutes une route /new côté back, tu peux l'appeler ici.)
 */
function resetBoard() {
state.grid = makeEmptyGrid(state.size);
renderBoardValues();
setStatus("Grille réinitialisée.");
log("Reset local du plateau.");
}

/* ============================================================================
 * Initialisation de la page
 * ========================================================================== */
(function init() {
buildBoardSkeleton();
renderBoardValues();

DOM.btnPlay.addEventListener("click", playTurn);
DOM.btnReset.addEventListener("click", resetBoard);

setStatus("Prêt. Configure le modèle et clique sur « Jouer ».");
})();
