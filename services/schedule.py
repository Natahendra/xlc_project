from sqlmodel import Session
from repositories.schedule import ScheduleRepository
from models.schedule import Schedule
from schemas.schedule import ScheduleCreate, ScheduleUpdate

class ScheduleService:
    def __init__(self, session: Session):
        self.repo = ScheduleRepository(session)

    def list_schedules(self):
        return self.repo.get_all()

    def get_schedule(self, schedule_id: int):
        schedule = self.repo.get_by_id(schedule_id)
        if not schedule:
            raise ValueError("Schedule not found")
        return schedule

    def create_schedule(self, schedule_in: ScheduleCreate):
        schedule = Schedule(**schedule_in.dict())
        return self.repo.create(schedule)

    def update_schedule(self, schedule_id: int, schedule_in: ScheduleUpdate):
        schedule = self.repo.get_by_id(schedule_id)
        if not schedule:
            raise ValueError("Schedule not found")
        for key, value in schedule_in.dict(exclude_unset=True).items():
            setattr(schedule, key, value)
        return self.repo.update(schedule)

    def delete_schedule(self, schedule_id: int):
        schedule = self.repo.get_by_id(schedule_id)
        if not schedule:
            raise ValueError("Schedule not found")
        self.repo.delete(schedule)
        return {"ok": True}
