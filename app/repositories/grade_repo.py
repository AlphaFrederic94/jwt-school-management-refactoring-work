# app/repositories/grade_repo.py
from sqlalchemy.orm import Session
from app.models.grade import Grade
from app.schema.grade_schema import GradeCreate

class GradeRepository:

    @staticmethod
    def get_grades_for_student(db: Session, student_id: int) -> Grade:
        return db.query(Grade).filter(Grade.student_id == student_id).first()

    @staticmethod
    def create_or_update_grades(db: Session, student_id: int, grade_data: GradeCreate) -> Grade:
        db_grade = db.query(Grade).filter(Grade.student_id == student_id).first()
        if db_grade:
            db_grade.pure_maths = grade_data.pure_maths
            db_grade.chemistry = grade_data.chemistry
            db_grade.biology = grade_data.biology
            db_grade.computer_science = grade_data.computer_science
            db_grade.physics = grade_data.physics
        else:
            db_grade = Grade(
                student_id=student_id,
                pure_maths=grade_data.pure_maths,
                chemistry=grade_data.chemistry,
                biology=grade_data.biology,
                computer_science=grade_data.computer_science,
                physics=grade_data.physics,
            )
            db.add(db_grade)
        
        db.commit()
        db.refresh(db_grade)
        return db_grade

    @staticmethod
    def get_top_students(db: Session, limit: int = 5):
        return db.execute(
            """
            SELECT u.id, u.first_name, u.last_name, u.email, u.date_of_birth,
                   (g.pure_maths + g.chemistry + g.biology + g.computer_science + g.physics) / 5 as avg_mark
            FROM users u
            JOIN grades g ON u.id = g.student_id
            ORDER BY avg_mark DESC
            LIMIT :limit
            """, {'limit': limit}
        ).fetchall()
    
    @staticmethod
    def delete_grades_by_student(student_id: int, db: Session): 
        db.query(Grade).filter(Grade.student_id == student_id).delete()
    