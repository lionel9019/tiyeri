document.addEventListener("DOMContentLoaded", () => {
  const API_BASE_URL = window.location.origin;
  const token = localStorage.getItem("access_tokenAdmin");

  const listContainer = document.getElementById("chat-memory-list");
  const form = document.getElementById("entry-form");
  const questionInput = document.getElementById("question");
  const answerInput = document.getElementById("answer");

  async function loadChatMemory() {
    try {
      const res = await fetch(`${API_BASE_URL}/admin/module/chat-memory`, {
        headers: {
          "Authorization": "Bearer " + token,
        },
      });

      if (!res.ok) throw new Error("Impossible de charger la mémoire");

      const data = await res.json();
      listContainer.innerHTML = "";

      Object.entries(data).forEach(([question, answer]) => {
        const li = document.createElement("li");
        li.innerHTML = `
          <strong>❓ ${question}</strong><br>
          <em>💬 ${answer}</em>
          <button class="edit">Modifier</button>
          <button class="delete">Supprimer</button>
        `;

        li.querySelector(".edit").onclick = () => {
          questionInput.value = question;
          answerInput.value = answer;
        };

        li.querySelector(".delete").onclick = async () => {
          if (confirm("Supprimer cette entrée ?")) {
            await fetch(`${API_BASE_URL}/admin/module/chat-memory?question=${encodeURIComponent(question)}`,
              {
                method: "DELETE",
                headers: {
                  "Authorization": "Bearer " + token,
                },
              }
            );
            loadChatMemory();
          }
        };

        listContainer.appendChild(li);
      });
    } catch (err) {
      listContainer.innerHTML = `<li style="color:red;">Erreur : ${err.message}</li>`;
    }
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = questionInput.value.trim();
    const answer = answerInput.value.trim();

    if (question && answer) {
      try {
        const res = await fetch(`${API_BASE_URL}/admin/module/chat-memory`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
          },
          body: JSON.stringify({ question, answer }),
        });

        if (!res.ok) throw new Error("Erreur lors de l'enregistrement");
        form.reset();
        loadChatMemory();
      } catch (err) {
        alert("Erreur : " + err.message);
      }
    }
  });

  loadChatMemory();

  // 🔁 Upload document
  const uploadForm = document.getElementById("upload-form");
  const fileInput = document.getElementById("doc-file"); // corrigé ici
  const uploadStatus = document.getElementById("upload-message"); // correspond à admin.html

  if (uploadForm) {
    uploadForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      if (!fileInput.files.length) {
        uploadStatus.textContent = "Veuillez sélectionner un fichier.";
        return;
      }

      if (!token) {
        uploadStatus.textContent = "Vous devez être connecté pour uploader un document.";
        return;
      }

      const file = fileInput.files[0];
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch(`${API_BASE_URL}/admin/upload-doc`, {
          method: "POST",
          headers: {
            "Authorization": "Bearer " + token,
          },
          body: formData,
        });

        if (!response.ok) {
          const text = await response.text();
          uploadStatus.textContent = `Erreur lors de l'upload : ${text}`;
          return;
        }

        const data = await response.json();
        uploadStatus.textContent = data.message || "✅ Document chargé avec succès.";
        fileInput.value = "";
      } catch (error) {
        uploadStatus.textContent = "❌ Erreur réseau : " + error.message;
      }
    });
  }
});
