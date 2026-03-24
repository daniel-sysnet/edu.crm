from typing import List, Optional
from datetime import date
from app.models.student import Student
from app.models.gender import Gender
from app.extensions import db
from sqlalchemy import desc

class StudentService:
    def addStudent(self, name: str, email: str, genre: Gender, birthday: date, 
                   adresse: str, telephone: str) -> Student:
        """Crée un étudiant. Le matricule est généré par le modèle ou la DB."""
        student = Student(
            name=name,
            email=email,
            gender=genre,
            dob=birthday,
            address=adresse,
            phone=telephone
        )
        db.session.add(student)
        db.session.commit()
        return student

    def deleteStudent(self, matricule: str) -> bool:
        """Supprime un étudiant par son matricule."""
        student = Student.query.filter_by(matricule=matricule).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return True
        return False

    def listStudents(self, query: str = None, genre: Gender = None) -> List[Student]:
        """Liste filtrée et triée par les plus récents."""
        stmt = Student.query
        if query:
            search = f"%{query}%"
            stmt = stmt.filter(
                (Student.name.ilike(search)) | 
                (Student.email.ilike(search)) |
                (Student.matricule.ilike(search))
            )
        if genre:
            stmt = stmt.filter(Student.gender == genre)
        
        return stmt.order_by(desc(Student.id)).all()

    def getByMatricule(self, matricule: str) -> Optional[Student]:
        """Récupère un étudiant par son matricule unique."""
        return Student.query.filter_by(matricule=matricule).first()

    def countStudents(self) -> int:
        return Student.query.count()

student_service = StudentService()