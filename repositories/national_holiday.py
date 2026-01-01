from sqlmodel import Session, select
from typing import List, Optional
from models.national_holiday import NationalHoliday

class NationalHolidayRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[NationalHoliday]:
        return self.session.exec(select(NationalHoliday)).all()

    def get_by_id(self, holiday_id: int) -> Optional[NationalHoliday]:
        return self.session.get(NationalHoliday, holiday_id)

    def create(self, holiday: NationalHoliday) -> NationalHoliday:
        self.session.add(holiday)
        self.session.commit()
        self.session.refresh(holiday)
        return holiday

    def update(self, holiday: NationalHoliday) -> NationalHoliday:
        self.session.add(holiday)
        self.session.commit()
        self.session.refresh(holiday)
        return holiday

    def delete(self, holiday: NationalHoliday):
        self.session.delete(holiday)
        self.session.commit()
