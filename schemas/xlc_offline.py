from pydantic import BaseModel
from typing import Optional
from datetime import date

class XlcOfflineBase(BaseModel):
    hostname2: Optional[str] = None
    location: Optional[str] = None
    store_name: Optional[str] = None
    hostname22: Optional[str] = None
    connection: Optional[str] = None
    region: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    tipe: Optional[str] = None
    location_status: Optional[str] = None
    network_priority: Optional[str] = None
    genset_status: Optional[str] = None
    ups_inventer_status: Optional[str] = None
    receiver_type: Optional[str] = None
    receiver_status: Optional[str] = None
    battery_backup_status: Optional[str] = None
    route_path: Optional[str] = None
    data_link: Optional[str] = None
    main_link: Optional[str] = None
    prot: Optional[str] = None
    site_id: Optional[str] = None
    affected_device: Optional[str] = None
    lease_expired: Optional[date] = None
    note: Optional[str] = None
    column1: Optional[str] = None
    host: Optional[str] = None
    column2: Optional[str] = None
    host3: Optional[str] = None
    activity_log: Optional[str] = None

class XlcOfflineCreate(XlcOfflineBase):
    pass

class XlcOfflineUpdate(XlcOfflineBase):
    pass

class XlcOfflineRead(XlcOfflineBase):
    id: int

    class Config:
        from_attributes = True
