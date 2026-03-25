from datetime import date
from typing import Optional
from app.models.student import Student
from app.models.gender import Gender
from app.extensions import db


class StudentService:
    def __init__(self):
        pass

    def addStudent(self, name: str, email: str, gender: Gender, birthday: date, adresse: str, telephone: str) -> Student:
        """Crée et ajoute un nouvel étudiant dans la base de données."""
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

    def deleteStudent(self, matricule: str) -> Optional[Student]:
        """Supprime un étudiant par matricule."""
        student = self.getByMatricule(matricule)
        if student is None:
            return None
        
        db.session.delete(student)
        db.session.commit()
        return student

    def updateStudent(self, matricule: str, name: str, email: str, gender: Gender, birthday: date, adresse: str, telephone: str) -> Optional[Student]:
        """Met à jour un étudiant existant par matricule."""
        student = self.getByMatricule(matricule)
        if student is None:
            return None
        
        student.name = name
        student.email = email
        student.gender = gender
        student.dob = birthday
        student.address = adresse
        student.phone = telephone
        
        db.session.commit()
        return student

    def listStudents(self, query: str = None, gender: Gender = None) -> list[Student]:
        """Liste tous les étudiants avec filtrage optionnel par recherche et genre."""
        # Récupération de tous les étudiants depuis la base de données
        students_query = Student.query

        # Filtrage par recherche textuelle (nom, email, matricule)
        if query:
            search_pattern = f"%{query.lower()}%"
            students_query = students_query.filter(
                db.or_(
                    Student.name.ilike(search_pattern),
                    Student.email.ilike(search_pattern),
                    Student.matricule.ilike(search_pattern)
                )
            )

        # Filtrage par genre
        if gender:
            students_query = students_query.filter(Student.gender == gender)

        # Retour sous forme de liste
        return students_query.all()

    def getByMatricule(self, matricule: str) -> Optional[Student]:
        """Récupère un étudiant par son matricule."""
        return Student.query.filter_by(matricule=matricule).first()

    def countStudents(self) -> int:
        """Compte le nombre total d'étudiants."""
        return Student.query.count()


student_service = StudentService()