from sqlmodel import Session
from repositories.xlc_offline import XlcOfflineRepository
from models.xlc_offline import XlcOffline
from schemas.xlc_offline import XlcOfflineCreate, XlcOfflineUpdate

class XlcOfflineService:
    def __init__(self, session: Session):
        self.repo = XlcOfflineRepository(session)

    def list_all(self):
        return self.repo.get_all()

    def get_by_id(self, xlc_id: int):
        xlc = self.repo.get_by_id(xlc_id)
        if not xlc:
            raise ValueError("XlcOffline not found")
        return xlc

    def create(self, xlc_in: XlcOfflineCreate):
        xlc = XlcOffline(**xlc_in.dict())
        return self.repo.create(xlc)

    def update(self, xlc_id: int, xlc_in: XlcOfflineUpdate):
        xlc = self.repo.get_by_id(xlc_id)
        if not xlc:
            raise ValueError("XlcOffline not found")
        for key, value in xlc_in.dict(exclude_unset=True).items():
            setattr(xlc, key, value)
        return self.repo.update(xlc)

    def delete(self, xlc_id: int):
        xlc = self.repo.get_by_id(xlc_id)
        if not xlc:
            raise ValueError("XlcOffline not found")
        self.repo.delete(xlc)
        return {"ok": True}
