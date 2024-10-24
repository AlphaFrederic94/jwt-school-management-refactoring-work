# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services.auth_service import authenticate_user, create_access_token, hash_password, get_current_user
from app.database.database import get_db
from app.schema.user_schema import UserCreate, UserResponse, UserUpdate
from app.repositories.user_repo import UserRepository
from datetime import timedelta
from jose import JWTError, jwt
from app.models.user import User

router = APIRouter()


@router.post("/login")  #login using the email and the password
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"email": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = UserRepository.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered") 
    hashed_password = hash_password(user_data.password)
    new_user = UserRepository.create_user(db, user_data, hashed_password)
    return new_user



def get_current_teacher(current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


def get_current_student(current_user:User= Depends(get_current_user)):
    if current_user.role != "student":
        raise HTTPException(status_code=500, detail="Only for students")
    return current_user


@router.get("/students")# to get all students
def get_students(db: Session= Depends(get_db)):
    students = UserRepository.get_all_students(db)
    if not students:
        raise
    HTTPException(status_code=404,detail="student not found")
    return students

@router.get("/teachers") # to get all teachers
def get_teachers(db: Session= Depends(get_db)):
    teachers = UserRepository.get_all_teachers(db)
    if not teachers:
        raise
    HTTPException(status_code=404,detail="student not found")
    return teachers

@router.put("/students/{student_id}")# to update a student
def update_student(student_id: int,student_update:UserUpdate ,db :Session = Depends(get_db), current_user: dict=Depends(get_current_user)):
    get_current_teacher(current_user)
    student = UserRepository.fetch_student(student_id,db)
    updates = student_update.dict(exclude_unset="true")
    updated_student = UserRepository.update_student_record(student, updates,db)
    return{"message":"student updated successfully","student":updated_student}

@router.delete("/students/{student_id}")# Deleting a student by id
def delete_student_and_grades(student_id: int , db: Session= Depends(get_db),current_user: dict = Depends(get_current_user)):
    get_current_teacher(current_user)
    student= UserRepository.fetch_student(student_id,db)
    UserRepository.delete_student_by_id(student_id,db)
    db.commit
    return{"message":"student deleted successfully"}
