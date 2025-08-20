import sqlite3

# Koneksi ke database SQLite, file database bernama questions.db
conn = sqlite3.connect('questions.db')
c = conn.cursor()

# Membuat tabel eskalasi pertanyaan jika belum ada
def setup_db():
    c.execute('''
    CREATE TABLE IF NOT EXISTS escalations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        question TEXT NOT NULL,
        status TEXT DEFAULT 'pending'
    )
    ''')
    conn.commit()

# Fungsi menyimpan pertanyaan
def simpan_pertanyaan(user, question):
    c.execute("INSERT INTO escalations (user, question) VALUES (?, ?)", (user, question))
    conn.commit()

# Fungsi mengambil pertanyaan pending
def ambil_pertanyaan_pending():
    c.execute("SELECT id, user, question FROM escalations WHERE status = 'pending'")
    return c.fetchall()

# Fungsi menandai pertanyaan selesai
def close_pertanyaan(id):
    c.execute("UPDATE escalations SET status = 'closed' WHERE id = ?", (id,))
    conn.commit()
