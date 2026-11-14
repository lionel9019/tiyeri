// ==========================
// Configuration
// ==========================
const API_BASE = "http://127.0.0.1:8000/api";

// ==========================
// Gestion du token utilisateur
// ==========================
function getToken() {
  const token = localStorage.getItem("access_token");
  console.log("🔑 getToken() →", token);
  return token;
}

function setToken(token) {
  console.log("💾 setToken() →", token);
  localStorage.setItem("access_token", token);
  console.log("📦 localStorage après set:", localStorage.getItem("access_token"));
}

function clearToken() {
  console.warn("🗑️ clearToken() appelé !");
  localStorage.removeItem("access_token");
  console.log("📦 localStorage après clear:", localStorage.getItem("access_token"));
}

// ==========================
// Requête générique avec token
// ==========================
async function apiFetch(endpoint, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
    console.log(`➡️ Appel API ${endpoint} avec token:`, token);
  } else {
    console.warn(`➡️ Appel API ${endpoint} SANS token`);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  console.log(`📡 Réponse [${endpoint}] → status:`, response.status);

  if (response.status === 401 && endpoint === "/users/me") {
    // 🚫 Si le problème est l’auth globale → on déconnecte
    console.error(`🚫 401 Unauthorized sur ${endpoint}, on efface le token.`);
    clearToken();
    window.location.href = "index.html";
    return {};
  }

  if (response.status === 401) {
    // ⚠️ Sinon on garde le token (cas subscription ou conversations)
    console.warn(`⚠️ 401 sur ${endpoint}, mais on ne supprime PAS le token`);
    return {};
  }

  return response.json().catch(() => ({}));
}


// ==========================
// Chargement des infos utilisateur
// ==========================
async function loadUser() {
  console.log("👤 Chargement utilisateur...");
  const data = await apiFetch("/users/me");
  console.log("👤 Données utilisateur:", data);

  if (data && data.username) {
    document.getElementById("username").innerText = data.username;
  }
}

// ==========================
// Chargement de l'abonnement
// ==========================
async function loadSubscription() {
  console.log("📦 Chargement abonnement...");
  const data = await apiFetch("http://127.0.0.1:8000/api/subscriptions/me");
  console.log("📦 Données abonnement:", data);

  if (data && data.plan) {
    document.getElementById("subscription").innerText = data.plan.name;
  } else {
    document.getElementById("subscription").innerText = "Aucun abonnement";
  }
}

// ==========================
// Chargement des conversations
// ==========================
async function loadConversations() {
  console.log("💬 Chargement conversations...");
  const data = await apiFetch("/conversations/");
  console.log("💬 Données conversations:", data);

  const container = document.getElementById("conversations");
  container.innerHTML = "";

  if (Array.isArray(data)) {
    data.forEach(conv => {
      const div = document.createElement("div");
      div.className = "conversation";
      div.innerText = conv.title || "Conversation sans titre";
      container.appendChild(div);
    });
  }
}

// ==========================
// Sauvegarde des préférences
// ==========================
async function savePreferences(prefs) {
  console.log("⚙️ Sauvegarde préférences:", prefs);
  const data = await apiFetch("/users/preferences", {
    method: "POST",
    body: JSON.stringify(prefs),
  });
  console.log("⚙️ Réponse préférences:", data);
}

// ==========================
// Initialisation page
// ==========================
document.addEventListener("DOMContentLoaded", async () => {
  console.log("🚀 Page chargée, initialisation...");
  await loadUser();
  await loadSubscription();
  await loadConversations();
});
