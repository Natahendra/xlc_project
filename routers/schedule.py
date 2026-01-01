from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from services.schedule import ScheduleService
from schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleRead
from lib.database import get_session

router = APIRouter(prefix="/schedules", tags=["schedules"])

@router.get("/", response_model=List[ScheduleRead])
def list_schedules(session: Session = Depends(get_session)):
    service = ScheduleService(session)
    return service.list_schedules()

@router.get("/{schedule_id}", response_model=ScheduleRead)
def get_schedule(schedule_id: int, session: Session = Depends(get_session)):
    service = ScheduleService(session)
    try:
        return service.get_schedule(schedule_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Schedule not found")

@router.post("/", response_model=ScheduleRead)
def create_schedule(schedule_in: ScheduleCreate, session: Session = Depends(get_session)):
    service = ScheduleService(session)
    return service.create_schedule(schedule_in)

@router.patch("/{schedule_id}", response_model=ScheduleRead)
def update_schedule(schedule_id: int, schedule_in: ScheduleUpdate, session: Session = Depends(get_session)):
    service = ScheduleService(session)
    try:
        return service.update_schedule(schedule_id, schedule_in)
    except ValueError:
        raise HTTPException(status_code=404, detail="Schedule not found")

@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, session: Session = Depends(get_session)):
    service = ScheduleService(session)
    try:
        return service.delete_schedule(schedule_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Schedule not found")
