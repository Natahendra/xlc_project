from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class NationalHoliday(SQLModel, table=True):
    __tablename__ = "national_holiday"

    id: Optional[int] = Field(default=None, primary_key=True)
    time: date
    note: Optional[str] = None
