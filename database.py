import sqlite3
from datetime import datetime

DB_NAME = "history.db"

# -------------------------------
# Inisialisasi Database
# -------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            registrar TEXT,
            malicious_count INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# -------------------------------
# Simpan Riwayat
# -------------------------------
def save_search_history(url, vt_summary, whois_registrar):
    try:
        malicious_count = vt_summary.get("malicious", 0)
        suspicious_count = vt_summary.get("suspicious", 0)

        status = "Aman"
        if malicious_count > 0:
            status = "Berbahaya"
        elif suspicious_count > 0:
            status = "Mencurigakan"

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO history (url, status, registrar, malicious_count, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (url, status, whois_registrar, malicious_count, datetime.now()))
        conn.commit()
        conn.close()
        print(f"✅ History saved for {url}")
        return True
    except Exception as e:
        print(f"❌ Error saving history: {e}")
        return False

# -------------------------------
# Ambil Riwayat
# -------------------------------
def get_search_history(limit=10):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, url, status, registrar, malicious_count, timestamp
            FROM history
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()

        history_list = []
        for row in rows:
            history_list.append({
                "id": row[0],
                "url": row[1],
                "status": row[2],
                "registrar": row[3],
                "malicious_count": row[4],
                "timestamp": row[5],
                "timestamp_human": datetime.fromisoformat(row[5]).strftime("%d %B %Y, %H:%M")
            })

        return history_list
    except Exception as e:
        print(f"❌ Error getting history: {e}")
        return []

# Panggil init_db saat modul diimpor
init_db()
