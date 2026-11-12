import requests
from bs4 import BeautifulSoup

def search_web(query: str, max_results=1) -> str:
    """
    Effectue une recherche web simplifiée via DuckDuckGo et retourne un résumé textuel.
    """
    try:
        # Préparer la requête de recherche
        url = f"https://html.google.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".result__snippet")

        if not results:
            return "Désolé, je n'ai pas trouvé de réponse pertinente sur Internet."

        # Prendre les premiers résultats valides
        snippets = [r.get_text().strip() for r in results[:max_results]]
        return "\n".join(snippets)

    except Exception as e:
        return f"Erreur lors de la recherche en ligne : {str(e)}"
