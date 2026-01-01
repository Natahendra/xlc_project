from sqlmodel import Session, select
from models.user import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(User)).all()

    def get_by_id(self, user_id: int):
        return self.session.get(User, user_id)

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def update(self, user: User, name: str | None = None, email: str | None = None):
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User):
        self.session.delete(user)
        self.session.commit()
