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

    @staticmethod
    def get_all_students(db: Session) -> User:
        return db.query(User).filter(User.role =='student').all()
    
    @staticmethod
    def get_all_teachers(db: Session) -> User:
        return db.query(User).filter(User.role =='teacher').all()
    
    @staticmethod
    def fetch_student(student_id:int , db:Session) -> User:
        student = db.query(User).filter(User.id == student_id, User.role =='student').first()
        return student
    
    @staticmethod
    def update_student_record(student: User, updates: dict, db:Session):
        for field, value in updates.items():
            setattr(student, field, value)
            db.commit()
            return student
        
    @staticmethod
    def delete_student_by_id(student_id: int, db: Session): 
        db.query(User).filter(User.id == student_id).delete()


    