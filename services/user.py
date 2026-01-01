from sqlmodel import Session
from repositories.user import UserRepository
from models.user import User

class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)

    def list_users(self):
        return self.repo.get_all()

    def get_user(self, user_id: int):
        return self.repo.get_by_id(user_id)

    def create_user(self, name: str, email: str):
        user = User(name=name, email=email)
        return self.repo.create(user)
    
    def update_user(self, user_id: int, name: str | None = None, email: str | None = None):
        user = self.repo.get_by_id(user_id)
        if not user:
            return None
        return self.repo.update(user, name, email)

    def delete_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if user:
            self.repo.delete(user)
        return user
