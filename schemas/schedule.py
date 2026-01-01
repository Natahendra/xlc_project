from pydantic import BaseModel
from typing import Optional
from datetime import time

class ScheduleBase(BaseModel):
    host_name: str
    store_name: str

    senin_open: Optional[time] = None
    senin_close: Optional[time] = None
    selasa_open: Optional[time] = None
    selasa_close: Optional[time] = None
    rabu_open: Optional[time] = None
    rabu_close: Optional[time] = None
    kamis_open: Optional[time] = None
    kamis_close: Optional[time] = None
    jumat_open: Optional[time] = None
    jumat_close: Optional[time] = None
    sabtu_open: Optional[time] = None
    sabtu_close: Optional[time] = None
    minggu_open: Optional[time] = None
    minggu_close: Optional[time] = None
    national_holiday_open: Optional[time] = None
    national_holiday_close: Optional[time] = None

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(ScheduleBase):
    pass

class ScheduleRead(ScheduleBase):
    id: int

    class Config:
        from_attributes = True
