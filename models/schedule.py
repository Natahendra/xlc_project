from pydantic import BaseModel
from typing import Optional, Dict
from datetime import time
from enum import Enum

# Enum untuk memastikan nama hari yang konsisten dan menghindari typo
class Day(str, Enum):
    senin = "senin"
    selasa = "selasa"
    rabu = "rabu"
    kamis = "kamis"
    jumat = "jumat"
    sabtu = "sabtu"
    minggu = "minggu"
    national_holiday = "national_holiday"

# Model untuk jam operasional harian
class OperatingHours(BaseModel):
    open: Optional[time] = None
    close: Optional[time] = None

class ScheduleBase(BaseModel):
    host_name: str
    store_name: str
    # Menggunakan Dictionary untuk memetakan setiap hari ke jam operasionalnya
    # Ini lebih fleksibel dan mudah diiterasi
    operating_hours: Dict[Day, OperatingHours] = {}

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    host_name: Optional[str] = None
    store_name: Optional[str] = None
    operating_hours: Optional[Dict[Day, OperatingHours]] = None

class ScheduleRead(ScheduleBase):
    id: int

