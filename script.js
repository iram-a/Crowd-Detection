const trainEl = document.getElementById("train");
const coachTemplate = document.getElementById("coachTemplate");
const connDot = document.getElementById("connDot");
const connText = document.getElementById("connText");
const lastUpdated = document.getElementById("lastUpdated");
const refreshBtn = document.getElementById("refreshBtn");
const autoToggle = document.getElementById("autoToggle");

const STATUS_MAP = {
  safe: { label: "Safe", color: "var(--safe)" },
  moderate: { label: "Moderate", color: "var(--moderate)" },
  overcrowded: { label: "Overcrowded", color: "var(--over)" },
};

let autoRefresh = true;
let intervalId = null;

function buildCoaches(count = 12) {
  for (let i = 1; i <= count; i++) {
    const node = coachTemplate.content.cloneNode(true);
    const coach = node.querySelector(".coach");
    coach.dataset.index = i;
    coach.querySelector(".badge").textContent = `C-${i}`;
    trainEl.appendChild(node);
  }
}

function updateUI(data) {
  const coaches = trainEl.querySelectorAll(".coach");
  data.forEach((status, idx) => {
    const c = coaches[idx];
    if (!c) return;
    const st = STATUS_MAP[status.level] || STATUS_MAP.safe;
    c.querySelector(".bar").style.background = st.color;
    c.querySelector(".statusText").textContent = st.label;
    c.querySelector(".occ").textContent = status.occupancy + "%";
  });
}

async function fetchStatus() {
  try {
    connDot.className = "dot warn";
    connText.textContent = "Updating…";
    const res = await fetch("http://127.0.0.1:5000/crowd_status");

    if (!res.ok) throw new Error("Bad response");
    const data = await res.json();
    updateUI(data);
    connDot.className = "dot ok";
    connText.textContent = "Live";
    lastUpdated.textContent = new Date().toLocaleTimeString();
  } catch (e) {
    console.error("Fetch error", e);
    connDot.className = "dot err";
    connText.textContent = "Offline";
  }
}

function startAuto() {
  if (intervalId) clearInterval(intervalId);
  if (autoRefresh) {
    intervalId = setInterval(fetchStatus, 5000);
  }
}

refreshBtn.addEventListener("click", fetchStatus);
autoToggle.addEventListener("change", (e) => {
  autoRefresh = e.target.checked;
  startAuto();
});

document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowRight") {
    document.getElementById("track").scrollBy({ left: 100, behavior: "smooth" });
  }
  if (e.key === "ArrowLeft") {
    document.getElementById("track").scrollBy({ left: -100, behavior: "smooth" });
  }
});

buildCoaches();
fetchStatus();
startAuto();
