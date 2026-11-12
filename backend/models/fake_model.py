# backend/models/fake_model.py

class FakeModel:
    """Classe simulant un modèle NLP pour génération de texte."""
    def generate(self, prompt: str) -> str:
        # Tu peux personnaliser les réponses selon tes besoins
        return f"[Réponse simulée] Prompt reçu : {prompt}"


# Instance globale à utiliser dans ton API
model = FakeModel()
