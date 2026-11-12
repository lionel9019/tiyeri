from duckduckgo_search import ddg

results = ddg("techniques de compostage biologique", max_results=5)

if not results:
    print("Aucun résultat trouvé.")
else:
    for res in results:
        print(f"🔎 {res['title']}\n➡️ {res['href']}\n")
