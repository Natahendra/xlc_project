from sqlmodel import Session, select
from typing import List, Optional
from models.schedule import Schedule

class ScheduleRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Schedule]:
        return self.session.exec(select(Schedule)).all()

    def get_by_id(self, schedule_id: int) -> Optional[Schedule]:
        return self.session.get(Schedule, schedule_id)

    def create(self, schedule: Schedule) -> Schedule:
        self.session.add(schedule)
        self.session.commit()
        self.session.refresh(schedule)
        return schedule

    def update(self, schedule: Schedule) -> Schedule:
        self.session.add(schedule)
        self.session.commit()
        self.session.refresh(schedule)
        return schedule

    def delete(self, schedule: Schedule):
        self.session.delete(schedule)
        self.session.commit()
