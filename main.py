from fastapi import FastAPI
from routers import user, schedule, xlc_offline, national_holiday

app = FastAPI()

app.include_router(user.router)
app.include_router(schedule.router)
app.include_router(xlc_offline.router)
app.include_router(national_holiday.router)