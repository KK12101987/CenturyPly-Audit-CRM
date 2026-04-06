#!/usr/bin/env python3
from flask import Flask, render_template, request, send_file
from pathlib import Path
import sqlite3, re

BASE = Path(__file__).parent
DB = BASE / "centuryply_audit.db"

# VERSION MANAGEMENT
def get_current_version():
    p = BASE / "version.txt"
    return p.read_text().strip() if p.exists() else "v4.2 Ultimate Build — 2025"

def increment_version():
    p = BASE / "version.txt"
    if not p.exists():
        p.write_text("v4.2 Ultimate Build — 2025")
    v = p.read_text().strip()
    m = re.search(r"v(\d+)\.(\d+)", v)
    if m:
        major, minor = map(int, m.groups())
        minor += 1
        newv = f"v{major}.{minor} Ultimate Build — 2025"
        p.write_text(newv)
        return newv
    return v

# PDF ENGINE
from report_generator import generate_full_pdf

# DB INIT
from db_utils import init_db
init_db()

# FLASK APP
app = Flask(__name__, template_folder=str(BASE / "templates"),
             static_folder=str(BASE / "static"))

@app.context_processor
def inject_version():
    return {'current_version': get_current_version()}

# ROUTES ----------------------------------------------------------

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scoring')
def scoring():
    return render_template('centuryply_audit_with_scoring_final.html')

@app.route('/upload_audit_history', methods=['GET','POST'])
def upload_audit_history():
    if request.method == 'GET':
        return render_template('upload_audit_history.html')

    f = request.files.get('file')
    if not f:
        return render_template('upload_audit_history.html',
                               error="No file selected")

    save_to = BASE / "uploads" / "uploaded_audits" / f.filename
    f.save(str(save_to))
    return render_template('upload_audit_history.html',
                           success="File uploaded successfully!")

@app.route('/bulk_update', methods=['GET','POST'])
def bulk_update():
    return render_template('bulk_update.html')

@app.route('/run_legacy', methods=['GET','POST'])
def run_legacy():
    import subprocess, sys
    script = BASE / "legacy" / "run_legacy_example.py"
    try:
        proc = subprocess.run([sys.executable, str(script)],
                              capture_output=True, text=True, timeout=30)
        out = proc.stdout + "\n" + proc.stderr
    except Exception as e:
        out = str(e)

    return render_template('legacy_output.html', output=out)

@app.route('/generate_report_from_db', methods=['GET','POST'])
def generate_report_from_db():
    auditor = request.form.get('auditorName') if request.method=='POST' else \
              request.args.get('auditorName','Unknown_Auditor')

    import pandas as pd
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM qa_logs", conn)

    out = BASE / "reports" / f"CenturyPly_QA_Report_{auditor.replace(' ','_')}.pdf"
    generate_full_pdf(df, out, auditor)

    return send_file(str(out), as_attachment=True)

# MAIN ------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
