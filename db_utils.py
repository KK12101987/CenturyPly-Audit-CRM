import sqlite3
from pathlib import Path

BASE = Path(__file__).parent
DB = BASE / "centuryply_audit.db"

def get_conn():
    return sqlite3.connect(DB)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS qa_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sl INTEGER,
        name TEXT,
        mobile_number TEXT,
        call_duration TEXT,
        call_date TEXT,
        audit_date TEXT,
        franchise TEXT,

        introduction INTEGER,
        project_registration INTEGER,
        product_pricing_requirement INTEGER,
        product_feedback INTEGER,
        cross_upsell INTEGER,
        marketing_benefit INTEGER,
        redemption INTEGER,
        call_closure INTEGER,
        gtm_adherence INTEGER,
        crm_update INTEGER,
        softskill INTEGER,

        total_score INTEGER,
        total INTEGER,
        percent REAL,
        audit_observation TEXT
    );
    """)

    conn.commit()
    conn.close()
