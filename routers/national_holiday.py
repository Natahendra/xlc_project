from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session

from services.national_holiday import NationalHolidayService
from schemas.national_holiday import NationalHolidayCreate, NationalHolidayUpdate, NationalHolidayRead
from lib.database import get_session

router = APIRouter( prefix="/national-holidays", tags=["National Holiday"])

@router.get("/", response_model=List[NationalHolidayRead])
def list_holidays(session: Session = Depends(get_session)):
    service = NationalHolidayService(session)
    return service.list_all()

@router.get("/{holiday_id}", response_model=NationalHolidayRead)
def get_holiday(holiday_id: int, session: Session = Depends(get_session)):
    service = NationalHolidayService(session)
    try:
        return service.get(holiday_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Holiday not found")

@router.post("/", response_model=NationalHolidayRead)
def create_holiday(holiday_in: NationalHolidayCreate, session: Session = Depends(get_session)):
    service = NationalHolidayService(session)
    return service.create(holiday_in)

@router.patch("/{holiday_id}", response_model=NationalHolidayRead)
def update_holiday(holiday_id: int, holiday_in: NationalHolidayUpdate, session: Session = Depends(get_session)):
    service = NationalHolidayService(session)
    try:
        return service.update(holiday_id, holiday_in)
    except ValueError:
        raise HTTPException(status_code=404, detail="Holiday not found")

@router.delete("/{holiday_id}")
def delete_holiday(holiday_id: int, session: Session = Depends(get_session)):
    service = NationalHolidayService(session)
    try:
        return service.delete(holiday_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Holiday not found")
