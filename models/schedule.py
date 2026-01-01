from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import time

class Schedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    host_name: str
    store_name: str

    # Senin
    senin_open: Optional[time] = None
    senin_close: Optional[time] = None

    # Selasa
    selasa_open: Optional[time] = None
    selasa_close: Optional[time] = None

    # Rabu
    rabu_open: Optional[time] = None
    rabu_close: Optional[time] = None

    # Kamis
    kamis_open: Optional[time] = None
    kamis_close: Optional[time] = None

    # Jumat
    jumat_open: Optional[time] = None
    jumat_close: Optional[time] = None

    # Sabtu
    sabtu_open: Optional[time] = None
    sabtu_close: Optional[time] = None

    # Minggu
    minggu_open: Optional[time] = None
    minggu_close: Optional[time] = None
    
    # National Holiday
    national_holiday_open: Optional[time] = None
    national_holiday_close: Optional[time] = None
