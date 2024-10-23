# app/models/grade.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    pure_maths = Column(Float)
    chemistry = Column(Float)
    biology = Column(Float)
    computer_science = Column(Float)
    physics = Column(Float)

    owner = relationship("User", back_populates="grades")