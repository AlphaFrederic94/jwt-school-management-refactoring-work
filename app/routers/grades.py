# app/routers/grade.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.grade import Grade
from app.schema.grade_schema import GradeCreate, GradeResponse
from app.routers.auth import get_current_teacher
from app.repositories.grade_repo import GradeRepository
from app.schema.user_schema import UserResponse
from app.models.user import User

router = APIRouter()

@router.post("grades/", response_model=GradeResponse)
def create_or_update_grade(grade_data: GradeCreate, db: Session = Depends(get_db), current_teacher: User = Depends(get_current_teacher)):
    grade = GradeRepository.create_or_update_grades(db, current_teacher.id, grade_data)
    return grade

@router.get("grades/student/{student_id}", response_model=GradeResponse)
def get_grades_for_student(student_id: int, db: Session = Depends(get_db), current_teacher: User = Depends(get_current_teacher)):
    grade = GradeRepository.get_grades_for_student(db, student_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grades not found")
    return grade

@router.get("grades/top-students", response_model=List[UserResponse])
def get_top_students(limit: int = 5, db: Session = Depends(get_db), current_teacher: User = Depends(get_current_teacher)):
    top_students = GradeRepository.get_top_students(db, limit)
    return top_students
