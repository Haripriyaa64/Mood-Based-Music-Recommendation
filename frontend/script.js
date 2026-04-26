const API_BASE = "http://127.0.0.1:5000";

// ── Mood → emoji map ─────────────────────────────────────────────────
const MOOD_EMOJI = {
  happy:    "😄",
  sad:      "💔",
  angry:    "😤",
  stressed: "😰",
  calm:     "😌",
  energetic:"⚡",
  neutral:  "🎵",
};

// ── DOM refs ──────────────────────────────────────────────────────────
const inputEl      = document.getElementById("userInput");
const loadingEl    = document.getElementById("loadingState");
const infoBar      = document.getElementById("infoBar");
const songsGrid    = document.getElementById("songsGrid");
const errorState   = document.getElementById("errorState");
const infoMood     = document.getElementById("infoMood");
const infoActivity = document.getElementById("infoActivity");
const energyFill   = document.getElementById("energyFill");
const infoQuery    = document.getElementById("infoQuery");

// ── Enter key ─────────────────────────────────────────────────────────
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") getSongs();
});

// ── Active mode pill tracking ─────────────────────────────────────────
let activePill = null;

function quickMode(text, btn) {
  inputEl.value = text;
  if (activePill) activePill.classList.remove("active");
  activePill = btn;
  btn.classList.add("active");
  getSongs();
}

// Clear active pill on manual input
inputEl.addEventListener("input", () => {
  if (activePill) { activePill.classList.remove("active"); activePill = null; }
});

// ── Main function ─────────────────────────────────────────────────────
async function getSongs() {
  const input = inputEl.value.trim();
  if (!input) {
    inputEl.focus();
    inputEl.style.borderColor = "var(--accent2)";
    setTimeout(() => inputEl.style.borderColor = "", 600);
    return;
  }

  // Show loading, hide others
  show(loadingEl);
  hide(infoBar);
  hide(songsGrid);
  hide(errorState);
  songsGrid.innerHTML = "";

  try {
    const res = await fetch(`${API_BASE}/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.details || `HTTP ${res.status}`);
    }

    const data = await res.json();
    hide(loadingEl);

    renderInfoBar(data);
    renderSongs(data.songs);

  } catch (err) {
    console.error(err);
    hide(loadingEl);
    show(errorState);
  }
}

// ── Info bar renderer ─────────────────────────────────────────────────
function renderInfoBar(data) {
  const mood  = data.mood || "neutral";
  const emoji = MOOD_EMOJI[mood] || "🎵";
  const acts  = (data.context?.activities || ["general"]).join(", ");
  const energy = data.filters?.energy ?? 0.5;

  infoMood.textContent     = `${emoji} ${mood}`;
  infoActivity.textContent = acts;
  infoQuery.textContent    = data.query || "—";
  infoQuery.title          = data.query || "";

  // Animate energy bar
  energyFill.style.width = "0%";
  requestAnimationFrame(() => {
    energyFill.style.width = `${Math.round(energy * 100)}%`;
  });

  show(infoBar);
}

// ── Songs renderer ────────────────────────────────────────────────────
function renderSongs(songs) {
  if (!songs || songs.length === 0) {
    songsGrid.innerHTML = `
      <div style="grid-column:1/-1;text-align:center;padding:48px;color:var(--muted)">
        <p style="font-size:32px;margin-bottom:12px">🎵</p>
        <p>No songs found. Try a different query.</p>
      </div>`;
    show(songsGrid);
    return;
  }

  songsGrid.innerHTML = songs.map((song, i) => `
    <div class="song-card" onclick="window.open('${escHtml(song.url)}', '_blank')">
      <div class="song-thumb">
        <img
          src="${escHtml(song.image)}"
          alt="${escHtml(song.name)}"
          loading="lazy"
          onerror="this.src='https://img.youtube.com/vi/default/mqdefault.jpg'"
        />
        <div class="play-overlay">
          <div class="play-btn">▶</div>
        </div>
      </div>
      <div class="song-info">
        <p class="song-title">${escHtml(song.name)}</p>
        <p class="song-artist">${escHtml(song.artist || "YouTube Music")}</p>
      </div>
      <div class="song-footer">
        <a class="yt-link" href="${escHtml(song.url)}" target="_blank" onclick="event.stopPropagation()">
          ▶ Open on YouTube
        </a>
        <div class="yt-dot"></div>
      </div>
    </div>
  `).join("");

  show(songsGrid);
}

// ── Helpers ───────────────────────────────────────────────────────────
function show(el) { el.classList.remove("hidden"); }
function hide(el) { el.classList.add("hidden"); }

function escHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}