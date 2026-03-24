from typing import List, Optional
from datetime import date
from app.enum_ui import gender
from app.models.student import Student
from app.extensions import db
from sqlalchemy import desc

class StudentService:
    def addStudent(self, name: str, email: str, genre: gender, birthday: date, 
                   adresse: str, telephone: str) -> Student:
        """Crée et ajoute un étudiant en base de données[cite: 181, 189]."""
        student = Student(
            name=name,
            email=email,
            gender=gender,
            dob=birthday,
            address=adresse,
            phone=telephone
        )
        db.session.add(student)
        db.session.commit()
        return student

    def deleteStudent(self, id: int) -> Optional[Student]:
        """Supprime un étudiant par son ID[cite: 182, 189]."""
        student = Student.query.get(id)
        if student:
            db.session.delete(student)
            db.session.commit()
        return student

    def listStudents(self, query: str = None, genre: gender = None) -> List[Student]:
        """Retourne la liste filtrée et triée par les plus récents[cite: 183, 184]."""
        stmt = Student.query
        
        if query:
            search = f"%{query}%"
            stmt = stmt.filter(
                (Student.name.ilike(search)) | 
                (Student.email.ilike(search))
            )
            
        if genre:
            stmt = stmt.filter(Student.genre == genre)
            
        # Tri par les plus récents (ID décroissant)
        return stmt.order_by(desc(Student.id)).all()

    def getById(self, id: int) -> Optional[Student]:
        """Retourne un étudiant par son ID[cite: 185, 189]."""
        return Student.query.get(id)

    def countStudents(self) -> int:
        """Retourne le nombre total d'étudiants[cite: 186, 189]."""
        return Student.query.count()

# Instance unique pour l'application
student_service = StudentService()