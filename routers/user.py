from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from lib.database import get_session
from services.user import UserService
from schemas.user import UserCreate, UserRead
from schemas.user import UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

# GET http://localhost:8000/users
@router.get("/", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    service = UserService(session)
    return service.list_users()

# GET http://localhost:8000/users/123
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    service = UserService(session)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# POST http://localhost:8000/users
@router.post("/", response_model=UserRead)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.create_user(user_in.name, user_in.email)

# PATCH http://localhost:8000/users
@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_in: UserUpdate, session: Session = Depends(get_session)):
    service = UserService(session)
    user = service.update_user(user_id, user_in.name, user_in.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# DELETE http://localhost:8000/users/123
@router.delete("/{user_id}", response_model=UserRead)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    service = UserService(session)
    user = service.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
