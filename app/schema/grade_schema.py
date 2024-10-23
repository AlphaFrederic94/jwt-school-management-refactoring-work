# app/schemas/grade_schema.py
from pydantic import BaseModel
from typing import Optional

class GradeCreate(BaseModel):
    pure_maths: float
    chemistry: float
    biology: float
    computer_science: float
    physics: float

class GradeResponse(BaseModel):
    id: int
    student_id: int
    pure_maths: float
    chemistry: float
    biology: float
    computer_science: float
    physics: float

    class Config:
        orm_mode = True