# app/repositories/user_repo.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user_schema import UserCreate

class UserRepository:

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate, hashed_password: str) -> User:
        db_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role,
            date_of_birth=user_data.date_of_birth,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()
