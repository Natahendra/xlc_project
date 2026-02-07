# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import mysql.connector
# from typing import Optional
# from datetime import datetime, timedelta  # <--- INI WAJIB ADA BIAR GAK ERROR

# app = FastAPI()

# # --- BIAR REACT BISA AKSES ---
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class LoginRequest(BaseModel):
#     id: str
#     password: str

# def get_db():
#     try:
#         return mysql.connector.connect(
#             host="localhost", 
#             user="root", 
#             password="", 
#             database="xlc_rewrite"
#         )
#     except Exception as e:
#         print(f"❌ DB CONNECTION ERROR: {e}")
#         return None

# # --- LOGIC TERBARU: HITUNG DETIK (ANTI ERROR DATA) ---
# def calculate_severity_seconds(row):
#     try:
#         now = datetime.now()
#         # Detik saat ini (WIB)
#         detik_sekarang = (now.hour * 3600) + (now.minute * 60) + now.second
        
#         # Ambil nama hari
#         hari_index = now.weekday() 
#         list_hari = ["senin", "selasa", "rabu", "kamis", "jumat", "sabtu", "minggu"]
#         hari_ini = list_hari[hari_index]
        
#         # Ambil data dari hasil JOIN
#         val_open = row.get(f"{hari_ini}_open")
#         val_close = row.get(f"{hari_ini}_close")

#         # JIKA DATA KOSONG (Gara-gara TYPO nama XLC/Hostname)
#         if val_open is None or val_close is None:
#             return "P3", ""

#         # Fungsi konversi timedelta ke detik
#         def convert_to_seconds(val):
#             if isinstance(val, timedelta):
#                 return val.total_seconds()
#             try: return float(val)
#             except: return 0

#         f_open = convert_to_seconds(val_open)
#         f_close = convert_to_seconds(val_close)

#         # Logic Severity: Cek waktu real-time
#         if f_open <= detik_sekarang <= f_close:
#             status = "P1"
#         else:
#             status = "P3"
            
#         # Format jam (HH:MM - HH:MM)
#         h_open, m_open = int(f_open // 3600), int((f_open % 3600) // 60)
#         h_close, m_close = int(f_close // 3600), int((f_close % 3600) // 60)
#         jam_info = f"{h_open:02d}:{m_open:02d} - {h_close:02d}:{m_close:02d}"
        
#         return status, jam_info

#     except Exception as e:
#         print(f"Error hitung severity: {e}")
#         return "P3", ""

# @app.get("/api/xlc")
# def search_xlc(q: Optional[str] = None):
#     try:
#         conn = get_db()
#         if not conn: return {"error": "Database Connection Failed"}
#         cursor = conn.cursor(dictionary=True)
        
#         # JOIN Site dengan Jadwal - Pake TRIM biar spasi gaib ilang
#         base_query = """
#             SELECT x.*, s.* FROM xlcoffline x 
#             LEFT JOIN schedule s ON TRIM(x.hostname2) = TRIM(s.host_name)
#         """
        
#         if q:
#             # Cari di banyak kolom sekaligus biar gak ribet
#             query = base_query + " WHERE x.store_name LIKE %s OR x.hostname2 LIKE %s OR x.location LIKE %s"
#             val = f"%{q}%"
#             cursor.execute(query, (val, val, val))
#         else:
#             cursor.execute(base_query + " LIMIT 20")
            
#         rows = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         for row in rows:
#             # Panggil fungsi hitung status
#             sev, info = calculate_severity_seconds(row)
#             row['severity'] = sev
#             row['jam_operasional'] = info
            
#             # Print di terminal biar Abang tenang liat datanya
#             print(f"DEBUG: {row.get('store_name')} | Status: {sev} | Jam: {info}")
            
#         return rows
#     except Exception as e:
#         print(f"❌ SYSTEM ERROR: {e}")
#         return {"error": str(e)}

# @app.post("/api/login")
# async def login(request: LoginRequest):
#     try:
#         conn = get_db()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT id, name FROM user WHERE id = %s", (request.id.strip(),))
#         user = cursor.fetchone()
#         cursor.close()
#         conn.close()
#         if user: return {"nama": user['name'], "id_user": user['id']}
#         raise HTTPException(status_code=404, detail="Gagal Login")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from typing import Optional
from datetime import datetime, timedelta

app = FastAPI()

# --- BIAR REACT BISA AKSES ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    id: str
    password: str

def get_db():
    try:
        return mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="", 
            database="xlc_rewrite"
        )
    except Exception as e:
        print(f"❌ DB CONNECTION ERROR: {e}")
        return None

# --- LOGIC TERBARU: HITUNG JAM & SEVERITY ---
def calculate_severity_seconds(row):
    try:
        now = datetime.now()
        # Detik saat ini (WIB)
        detik_sekarang = (now.hour * 3600) + (now.minute * 60) + now.second
        
        # Ambil nama hari
        hari_index = now.weekday() 
        list_hari = ["senin", "selasa", "rabu", "kamis", "jumat", "sabtu", "minggu"]
        hari_ini = list_hari[hari_index]
        
        # Ambil data dari hasil JOIN
        val_open = row.get(f"{hari_ini}_open")
        val_close = row.get(f"{hari_ini}_close")

        # JIKA DATA KOSONG (Berarti Hostname DAN Store Name gak ada yang cocok)
        if not val_open or not val_close:
            return "P3", "-"

        # --- FUNGSI SAKTI: KONVERSI JAM ---
        def parse_time_to_seconds(val):
            try:
                # Kalau formatnya string "08:30" (Ini yang Abang pake sekarang)
                if isinstance(val, str) and ":" in val:
                    h, m = map(int, val.split(":"))
                    return (h * 3600) + (m * 60)
                # Kalau formatnya Timedelta (bawaan MySQL lama)
                if isinstance(val, timedelta):
                    return val.total_seconds()
                # Kalau formatnya Angka/Float
                return float(val)
            except:
                return 0

        f_open = parse_time_to_seconds(val_open)
        f_close = parse_time_to_seconds(val_close)

        # Cek kalau tutup (0 detik atau 00:00)
        if f_open == 0 and f_close == 0:
             return "P3", "CLOSED"

        # Logic Severity: Cek waktu real-time
        if f_open <= detik_sekarang <= f_close:
            status = "P1"
        else:
            status = "P3"
            
        # Format jam buat ditampilin (HH:MM - HH:MM)
        h_open, m_open = int(f_open // 3600), int((f_open % 3600) // 60)
        h_close, m_close = int(f_close // 3600), int((f_close % 3600) // 60)
        jam_info = f"{h_open:02d}:{m_open:02d} - {h_close:02d}:{m_close:02d}"
        
        return status, jam_info

    except Exception as e:
        print(f"Error hitung severity: {e}")
        return "P3", "-"

@app.get("/api/xlc")
def search_xlc(q: Optional[str] = None):
    try:
        conn = get_db()
        if not conn: return {"error": "Database Connection Failed"}
        cursor = conn.cursor(dictionary=True)
        
        # --- QUERY JOIN PALING SAKTI (UPPER + TRIM) ---
        # Logika: 
        # 1. Hapus Spasi (TRIM)
        # 2. Ubah jadi HURUF BESAR SEMUA (UPPER) biar "Karawang" == "KARAWANG"
        # 3. Cari lewat Hostname DULU, atau (OR) lewat Nama Toko
        base_query = """
            SELECT x.*, s.* FROM xlcoffline x 
            LEFT JOIN schedule s ON (
                TRIM(UPPER(x.hostname2)) = TRIM(UPPER(s.host_name)) 
                OR 
                TRIM(UPPER(x.store_name)) = TRIM(UPPER(s.store_name))
            )
        """
        
        if q:
            # Bersihkan query search juga
            clean_q = q.strip()
            # Cari di banyak kolom sekaligus
            query = base_query + " WHERE x.store_name LIKE %s OR x.hostname2 LIKE %s OR x.location LIKE %s"
            val = f"%{clean_q}%"
            cursor.execute(query, (val, val, val))
        else:
            cursor.execute(base_query + " LIMIT 20")
            
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in rows:
            # Panggil fungsi hitung status
            sev, info = calculate_severity_seconds(row)
            row['severity'] = sev
            row['jam_operasional'] = info
            
            # --- DEBUG DI TERMINAL (BIAR ABANG TAU DATA MASUK APA ENGGAK) ---
            if info != "-":
                print(f"✅ MATCH: {row.get('store_name')} | Jam: {info}")
            else:
                print(f"❌ NO MATCH: {row.get('store_name')} (Cek Database Schedule!)")
            
        return rows
    except Exception as e:
        print(f"❌ SYSTEM ERROR: {e}")
        return {"error": str(e)}

@app.post("/api/login")
async def login(request: LoginRequest):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM user WHERE id = %s", (request.id.strip(),))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user: return {"nama": user['name'], "id_user": user['id']}
        raise HTTPException(status_code=404, detail="Gagal Login")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))