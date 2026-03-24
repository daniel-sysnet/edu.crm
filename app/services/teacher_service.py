from typing import Optional, List
from app.models.teacher import Teacher
from app.models.gender import Gender
from app.models.speciality import Speciality
from datetime import date
from app.extensions import db
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError


class TeacherService:

    def addTeacher(self, name: str, email: str, speciality, gender, dob: date | None,
                address: str, phone: str) -> Teacher:
        # Convertir en Enum si des chaînes sont fournies depuis le formulaire
        if isinstance(speciality, str):
            speciality = Speciality(speciality)
        if isinstance(gender, str):
            gender = Gender(gender)

        teacher = Teacher()
        teacher.name = name
        teacher.email = email
        teacher.speciality = speciality
        teacher.gender = gender
        teacher.dob = dob
        teacher.address = address
        teacher.phone = phone

        try:
            db.session.add(teacher)
            db.session.commit()
            return teacher
        except IntegrityError as e:
            db.session.rollback()  # ⚠️ indispensable, sinon la session est corrompue
            raise e  # on laisse la route gérer l’affichage (erreur unique/email déjà existant)


    def listTeachers(
        self,
        query: Optional[str] = None,
        gender: Optional[Gender] = None,
        speciality: Optional[Speciality] = None,
    ) -> List[Teacher]:
        q = Teacher.query
        if query:
            q = q.filter(
                (Teacher.name.ilike(f'%{query}%')) |
                (Teacher.email.ilike(f'%{query}%')) |
                (Teacher.matricule.ilike(f'%{query}%'))
            )
        if gender:
            q = q.filter(Teacher.gender == gender)
        if speciality:
            q = q.filter(Teacher.speciality == speciality)
        return q.order_by(desc(Teacher.created_at)).all()

    def getById(self, id: int) -> Optional[Teacher]:
        return Teacher.query.get(id)

    def countTeachers(self) -> int:
        return Teacher.query.count()

    def countWithoutCourses(self, course_service) -> int:
        return Teacher.query.filter(~Teacher.courses.any()).count()
    
    def getByMatricule(self, mat: str) -> Optional[Teacher]:
        return Teacher.query.filter_by(matricule=mat).first()
    
    def deleteTeacher(self, id: int) -> Optional[Teacher]:
        teacher = Teacher.query.get(id)
        if teacher:
            db.session.delete(teacher)
            db.session.commit()
            return teacher
        return None