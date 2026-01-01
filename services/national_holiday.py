from sqlmodel import Session
from repositories.national_holiday import NationalHolidayRepository
from schemas.national_holiday import NationalHolidayCreate, NationalHolidayUpdate
from models.national_holiday import NationalHoliday

class NationalHolidayService:
    def __init__(self, session: Session):
        self.repo = NationalHolidayRepository(session)

    def list_all(self):
        return self.repo.get_all()

    def get(self, holiday_id: int):
        holiday = self.repo.get_by_id(holiday_id)
        if not holiday:
            raise ValueError("National holiday not found")
        return holiday

    def create(self, holiday_in: NationalHolidayCreate):
        holiday = NationalHoliday(**holiday_in.dict())
        return self.repo.create(holiday)

    def update(self, holiday_id: int, holiday_in: NationalHolidayUpdate):
        holiday = self.repo.get_by_id(holiday_id)
        if not holiday:
            raise ValueError("National holiday not found")

        for key, value in holiday_in.dict(exclude_unset=True).items():
            setattr(holiday, key, value)

        return self.repo.update(holiday)

    def delete(self, holiday_id: int):
        holiday = self.repo.get_by_id(holiday_id)
        if not holiday:
            raise ValueError("National holiday not found")

        self.repo.delete(holiday)
        return {"ok": True}
