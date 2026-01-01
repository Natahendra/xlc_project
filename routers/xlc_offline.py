from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from services.xlc_offline import XlcOfflineService
from schemas.xlc_offline import XlcOfflineCreate, XlcOfflineUpdate, XlcOfflineRead
from lib.database import get_session

router = APIRouter(prefix="/xlcoffline", tags=["XlcOffline"])

@router.get("/", response_model=List[XlcOfflineRead])
def list_xlc(session: Session = Depends(get_session)):
    service = XlcOfflineService(session)
    return service.list_all()

@router.get("/{xlc_id}", response_model=XlcOfflineRead)
def get_xlc(xlc_id: int, session: Session = Depends(get_session)):
    service = XlcOfflineService(session)
    try:
        return service.get_by_id(xlc_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="XlcOffline not found")

@router.post("/", response_model=XlcOfflineRead)
def create_xlc(xlc_in: XlcOfflineCreate, session: Session = Depends(get_session)):
    service = XlcOfflineService(session)
    return service.create(xlc_in)

@router.patch("/{xlc_id}", response_model=XlcOfflineRead)
def update_xlc(xlc_id: int, xlc_in: XlcOfflineUpdate, session: Session = Depends(get_session)):
    service = XlcOfflineService(session)
    try:
        return service.update(xlc_id, xlc_in)
    except ValueError:
        raise HTTPException(status_code=404, detail="XlcOffline not found")

@router.delete("/{xlc_id}")
def delete_xlc(xlc_id: int, session: Session = Depends(get_session)):
    service = XlcOfflineService(session)
    try:
        return service.delete(xlc_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="XlcOffline not found")
