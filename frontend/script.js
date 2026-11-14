document.addEventListener("DOMContentLoaded", () => {
  const API_BASE_URL = window.location.origin;

  const loginSection = document.getElementById("login-section");
  const registerSection = document.getElementById("register-section");

  document.getElementById("show-register-btn").onclick = () => {
    loginSection.style.display = "none";
    registerSection.style.display = "block";
  };

  document.getElementById("show-login-btn").onclick = () => {
    registerSection.style.display = "none";
    loginSection.style.display = "block";
  };

  // 🔐 Inscription
  document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value.trim();

    if (!email || !password) {
      alert("Veuillez remplir tous les champs.");
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/users/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const contentType = response.headers.get("content-type") || "";
      if (!contentType.includes("application/json")) {
        const text = await response.text();
        throw new Error("Réponse inattendue du serveur : " + text);
      }

      const data = await response.json();

      if (!response.ok) throw new Error(data.detail || "Erreur lors de l'inscription.");

      alert(data.message || "Inscription réussie !");
      registerSection.style.display = "none";
      loginSection.style.display = "block";
    } catch (err) {
      console.error("Erreur d’inscription :", err);
      alert("Erreur d’inscription : " + err.message);
    }
  });

  // 🔓 Connexion
  document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value.trim();

    if (!email || !password) {
      alert("Veuillez remplir tous les champs.");
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/users/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username: email, password }),
      });

      const data = await response.json().catch(async () => {
        const text = await response.text();
        throw new Error("Réponse inattendue du serveur : " + text);
      });

      if (!response.ok) throw new Error(data.detail || "Identifiants incorrects.");

      if (data.access_token) {
        localStorage.setItem("access_token", data.access_token);
        alert("Connexion réussie !");
        window.location.href = "/accueil.html"; // ajuste si besoin
      } else {
        alert("Réponse invalide du serveur");
      }
    } catch (err) {
      console.error("Erreur de connexion :", err);
      alert("Erreur de connexion : " + err.message);
    }
  });
});
