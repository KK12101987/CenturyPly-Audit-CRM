@echo off
setlocal
echo == CenturyPly v4.2 Builder ==
echo Checking for Python...
python --version >nul 2>&1 || (
  echo Python is not available in PATH. Please install Python 3.10+ and ensure 'python' is on PATH.
  pause
  exit /b 1
)

REM ensure version file
if not exist version.txt echo v4.2 Ultimate Build — 2025> version.txt
echo Incrementing version...
python - <<END
import re, pathlib
p=pathlib.Path('version.txt')
v=p.read_text().strip()
m=re.search(r'v(\d+)\.(\d+)', v)
if m:
    major=int(m.group(1)); minor=int(m.group(2))+1
    new=f"v{major}.{minor} Ultimate Build — 2025"
else:
    new=v
p.write_text(new)
print("✅ Version updated to", new)
END

echo Installing dependencies (may take a few minutes)...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Starting Flask app on port 8080...
start "" python centuryply_audit_webapp.py
echo Done.
pause
