const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");
const logEl = document.getElementById("log");
const apiBaseEl = document.getElementById("apiBase");
const modelNameEl = document.getElementById("modelName");
const activePlayerEl = document.getElementById("activePlayer");
const btnPlay = document.getElementById("btnPlay");
const btnReset = document.getElementById("btnReset");

// 10×10 "", "X", "O"
let grid = Array.from({length:10},()=>Array(10).fill(""));

function log(x){
  const s = typeof x === "string" ? x : JSON.stringify(x, null, 2);
  logEl.textContent = s + "\n" + logEl.textContent;
}
function setStatus(msg){ statusEl.textContent = msg; }

function buildBoard(){
  boardEl.innerHTML = "";
  const thead = document.createElement("thead");
  const thr = document.createElement("tr");
  thr.appendChild(document.createElement("th"));
  for(let c=0;c<10;c++){
    const th = document.createElement("th");
    th.textContent = String.fromCharCode(65+c);
    thr.appendChild(th);
  }
  thead.appendChild(thr);
  boardEl.appendChild(thead);

  const tbody = document.createElement("tbody");
  for(let r=0;r<10;r++){
    const tr = document.createElement("tr");
    const th = document.createElement("th");
    th.textContent = r+1;
    tr.appendChild(th);
    for(let c=0;c<10;c++){
      const td = document.createElement("td");
      td.dataset.row = r; td.dataset.col = c;
      td.textContent = grid[r][c];
      tr.appendChild(td);
    }
    tbody.appendChild(tr);
  }
  boardEl.appendChild(tbody);
}
function renderBoard(){
  boardEl.querySelectorAll("td").forEach(td=>{
    const r = +td.dataset.row, c = +td.dataset.col;
    td.textContent = grid[r][c] || "";
  });
}

async function playOnce(){
  const API = apiBaseEl.value || "http://127.0.0.1:8000";
  const payload = {
    grid,
    active_player: activePlayerEl.value,     // "X" ou "O"
    model_name: modelNameEl.value || "llama3.2:1b"
  };

  setStatus("Requête en cours…");
  try{
    const res = await fetch(`${API}/play`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });
    const text = await res.text();
    let out;
    try { out = JSON.parse(text); } catch { throw new Error("Réponse non-JSON: "+text); }
    if(!res.ok) throw new Error(out?.detail || res.statusText);

    grid = out.grid;          // <- respecte PlayResponse
    renderBoard();

    setStatus(`Statut: ${out.status} — coup=(${out.move.row},${out.move.col})`);
    log({request: payload, response: out});

    if(out.status === "continue"){
      activePlayerEl.value = (activePlayerEl.value === "X") ? "O" : "X";
    }
  }catch(err){
    setStatus("Erreur: "+err.message);
    log(String(err));
  }
}

function resetBoard(){
  grid = Array.from({length:10},()=>Array(10).fill(""));
  renderBoard();
  setStatus("Grille réinitialisée.");
}

btnPlay.addEventListener("click", playOnce);
btnReset.addEventListener("click", resetBoard);

buildBoard();
renderBoard();
setStatus("Prêt. Clique « Jouer ».");

