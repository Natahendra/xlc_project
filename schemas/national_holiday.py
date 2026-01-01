from pydantic import BaseModel
from datetime import date
from typing import Optional

class NationalHolidayBase(BaseModel):
    time: date
    note: Optional[str] = None

class NationalHolidayCreate(NationalHolidayBase):
    pass

class NationalHolidayUpdate(BaseModel):
    time: Optional[date] = None
    note: Optional[str] = None

class NationalHolidayRead(NationalHolidayBase):
    id: int

    class Config:
        from_attributes = True
