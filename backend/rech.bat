@echo off
echo 🔎 Recherche de "chatbot_resources" dans tous les fichiers Python...
echo -------------------------------------------------------------
for /r %%f in (*.py) do (
    findstr /n /c:"chatbot_resources" "%%f" >nul
    if %errorlevel%==0 (
        echo ✅ Trouvé dans : %%f
        findstr /n /c:"chatbot_resources" "%%f"
        echo -------------------------------------------------------------
    )
)
echo 🔍 Recherche terminée.
pause
