# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.services.auth_service import authenticate_user, create_access_token, hash_password
from app.database.database import get_db
from app.schema.user_schema import UserCreate, UserResponse, UserUpdate
from app.repositories.user_repo import UserRepository
from datetime import timedelta
from jose import JWTError, jwt
from app.models.user import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "8d9d1e837bc56b07f7e1db15fe3a69b02b8c3a8f7f9261dcb7f556b5261a97ba"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/login")
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

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = UserRepository.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

def get_current_teacher(current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


def get_current_student(current_user:User= Depends(get_current_user)):
    if current_user.role != "student":
        raise HTTPException(status_code=500, detail="Only for students")
    return current_user


@router.get("/students")
def get_students(db: Session= Depends(get_db)):
    students = UserRepository.get_all_students(db)
    if not students:
        raise
    HTTPException(status_code=404,detail="student not found")
    return students

@router.put("/students/{student_id}")
def update_student(student_id: int,student_update:UserUpdate ,db :Session = Depends(get_db), current_user: dict=Depends(get_current_user)):
    get_current_teacher(current_user)
    student = UserRepository.fetch_student(student_id,db)
    updates = student_update.dict(exclude_unset="true")
    updated_student = UserRepository.update_student_record(student, updates,db)
    return{"message":"student updated successfully","student":updated_student}

@router.delete("/students/{student_id}")
def delete_student_and_grades(student_id: int , db: Session= Depends(get_db),current_user: dict = Depends(get_current_user)):
    get_current_teacher(current_user)
    student= UserRepository.fetch_student(student_id,db)
    UserRepository.delete_student_by_id(student_id,db)
    db.commit
    return{"message":"student deleted successfully"}
