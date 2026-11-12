import wikipedia

def search_wikipedia(query: str, lang: str = "fr") -> str:
    try:
        wikipedia.set_lang(lang)
        summary = wikipedia.summary(query, sentences=2)
        return f"📘 {summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        return f"🔍 Le terme est ambigu : {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return None
    except Exception as ex:
        print(f"[Erreur Wikipedia] {ex}")
        return None
