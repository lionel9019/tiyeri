@echo off
setlocal

REM === Dossier de recherche ===
set SEARCH_DIR=frontend
set OUTPUT_FILE=%SEARCH_DIR%\token_search_results.txt

echo Recherche des occurrences de "token" dans %SEARCH_DIR% > %OUTPUT_FILE%
echo ================================================= >> %OUTPUT_FILE%

for /R %SEARCH_DIR% %%f in (*.*) do (
    findstr /I /N token "%%f" >> %OUTPUT_FILE%
)

echo.
echo Résultats sauvegardés dans %OUTPUT_FILE%
pause
