import sqlite3

conn = sqlite3.connect('xlc_rewrite.db') 
cursor = conn.cursor()

# 1. BUAT TABEL USER DULU (Agar tidak error "no such table")
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id TEXT PRIMARY KEY,
    nama TEXT
)
''')

# 2. MASUKKAN ID OPERATOR
users = [
    ('iwx711559', 'I Gede Ari Hendra Nata'),
    ('m84250562', 'Muhamad Ari Rahmanto')
]

cursor.executemany("INSERT OR REPLACE INTO user (id, nama) VALUES (?, ?)", users)
conn.commit()
conn.close()
print("✅ Database Terupdate! Tabel user sudah dibuat dan diisi.")