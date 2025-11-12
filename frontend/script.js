const urlAPI = "http://127.0.0.1:8000/play";
const gridSize = 10;
let grid = Array.from({ length: gridSize }, () => Array(gridSize).fill(""));
let activePlayer = "X";
let modelName = "llama3.2:1b";
let isPlaying = false;

const gridHTML = document.querySelector("#grid");
const playerHTML = document.querySelector("#player");
const playBtn = document.querySelector("#play");
const resetBtn = document.querySelector("#reset");

function renderGrid() {
  gridHTML.innerHTML = "";
  for (let r = 0; r < gridSize; r++) {
    for (let c = 0; c < gridSize; c++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      if (grid[r][c] === "X" || grid[r][c] === "O") {
        cell.classList.add(grid[r][c]);
        cell.textContent = grid[r][c];
      }
      gridHTML.appendChild(cell);
    }
  }
}

function playTurn() {
  if (!isPlaying) return;

  playerHTML.textContent = `${activePlayer === "X" ? "Ollama" : "Azure"} place sont coup...`;

  fetch(urlAPI, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      grid: grid,
      active_player: activePlayer,
      model_name: modelName
    })
  })
    .then(res => res.json())
    .then(data => {
      console.log("Réponse:", data);
      grid = data.grid;
      renderGrid();

      if (data.status === "win") {
        playerHTML.textContent = `🎉 Victoire de ${activePlayer === "X" ? "Ollama" : "Azure"} !`;
        isPlaying = false;
      } else if (data.status === "draw") {
        playerHTML.textContent = "🤝 Match nul !";
        isPlaying = false;
      } else {
        // Prochain joueur
        activePlayer = activePlayer === "X" ? "O" : "X";
        modelName = modelName === "llama3.2:1b" ? "o4-mini" : "llama3.2:1b";
        setTimeout(playTurn, 1000); // délai entre les tours
      }
    })
    .catch(err => {
      console.error("Erreur:", err);
      playerHTML.textContent = "⚠️ Erreur de communication avec le backend";
      isPlaying = false;
    });
}

playBtn.addEventListener("click", () => {
  if (isPlaying) return;
  isPlaying = true;
  activePlayer = "X";
  modelName = "llama3.2:1b";
  playerHTML.textContent = " Le match commence !";
  playTurn();
});

resetBtn.addEventListener("click", () => {
  grid = Array.from({ length: gridSize }, () => Array(gridSize).fill(""));
  activePlayer = "X";
  modelName = "llama3.2:1b";
  isPlaying = false;
  renderGrid();
  playerHTML.textContent = "Grille réinitialisée. Clique sur 'Jouer' pour recommencer !";
});

renderGrid();
