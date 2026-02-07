import pandas as pd
import sqlite3
import os

# --- KONFIGURASI ---
CSV_FILE = 'Book1.csv'
DB_FILE = 'xlc_rewrite.db'

def setup_database():
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: File {CSV_FILE} tidak ditemukan!")
        return

    print("📖 Membaca dan membersihkan header CSV secara otomatis...")
    try:
        # 1. Baca CSV
        df = pd.read_csv(CSV_FILE, encoding='cp1252')

        # 2. OTOMATISASI: Mengubah header berantakan jadi standar database
        # Contoh: "Store Name" -> "store_name", "UPS/Inventer Status" -> "ups_inventer_status"
        df.columns = (
            df.columns.str.strip()             # Hapus spasi di awal/akhir
            .str.lower()                       # Jadi huruf kecil semua
            .str.replace(' ', '_')             # Spasi jadi underscore
            .str.replace('/', '_')             # Tanda miring jadi underscore
            .str.replace('.', '')              # Hapus titik
        )

        

        # 4. Pastikan kolom wajib ada agar React tidak error
        required = ['store_name', 'province', 'hostname22', 'hostname2', 'route_path']
        for col in required:
            if col not in df.columns:
                print(f"⚠️ Warning: Kolom {col} tidak ditemukan, membuat kolom kosong.")
                df[col] = "-"

        # 5. Masukkan ke Database
        conn = sqlite3.connect(DB_FILE)
        
        # Hapus tabel lama agar struktur baru masuk
        conn.execute("DROP TABLE IF EXISTS xlcoffline")
        
        # Simpan ke SQL
        # index=True dan index_label='id' sangat penting agar SQLAlchemy di Backend tidak error
        df.to_sql('xlcoffline', conn, if_exists='replace', index=True, index_label='id')
        
        conn.commit()
        conn.close()
        
        print("-" * 30)
        print(f"✅ BERHASIL! {len(df)} baris data masuk.")
        print(f"📊 Kolom yang tersedia: {', '.join(df.columns.tolist())}")
        print("-" * 30)

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")

if __name__ == "__main__":
    setup_database()