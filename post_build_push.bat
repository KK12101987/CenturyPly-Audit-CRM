@echo off
echo == post_build_push ==
git status >nul 2>&1
if errorlevel 1 (
  echo Git not initialized. Initializing repo...
  git init
  git branch -M main
)
git add .
git commit -m "Auto commit - CenturyPly QA v4.2 Ultimate Build" 2>nul || echo No changes to commit
echo Now pushing to origin (ensure remote is set and credentials available)...
git push origin main
echo Done.
pause
