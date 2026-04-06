@echo off
echo == Building Standalone CenturyPly QA WebApp EXE ==
echo Creating virtual environment...

python -m venv venv
call venv\Scripts\activate

echo Installing dependencies into venv...
pip install -r requirements.txt
pip install pyinstaller

echo Building EXE (this may take 1–3 minutes)...

pyinstaller --noconfirm ^
    --onefile ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "db_utils.py;." ^
    --icon=static/logo.ico ^
    centuryply_audit_webapp.py

echo Build complete. EXE is in /dist folder.
pause
