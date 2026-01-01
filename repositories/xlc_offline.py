from sqlmodel import Session, select
from typing import List, Optional
from models.xlc_offline import XlcOffline

class XlcOfflineRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[XlcOffline]:
        return self.session.exec(select(XlcOffline)).all()

    def get_by_id(self, xlc_id: int) -> Optional[XlcOffline]:
        return self.session.get(XlcOffline, xlc_id)

    def create(self, xlc: XlcOffline) -> XlcOffline:
        self.session.add(xlc)
        self.session.commit()
        self.session.refresh(xlc)
        return xlc

    def update(self, xlc: XlcOffline) -> XlcOffline:
        self.session.add(xlc)
        self.session.commit()
        self.session.refresh(xlc)
        return xlc

    def delete(self, xlc: XlcOffline):
        self.session.delete(xlc)
        self.session.commit()
