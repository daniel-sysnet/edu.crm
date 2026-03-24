from typing import Optional
from app.models.teacher import Teacher
from app.models.gender import Gender
from app.models.speciality import Speciality
from datetime import date


class TeacherService:

    def __init__(self):
        self.__teachers: list[Teacher] = []

    def addTeacher(self, name: str, email: str, specialty: Speciality,
                gender: Gender, birthday: date,
                adresse: str, telephone: str) -> Teacher:
        teacher = Teacher(
            name=name,
            email=email,
            specialty=specialty,
            gender=gender,
            birthday=birthday,
            adresse=adresse,
            telephone=telephone
        )
        self.__teachers.append(teacher)
        return teacher

    def deleteTeacher(self, id: int) -> Optional[Teacher]:
        for i, teacher in enumerate(self.__teachers):
            if teacher.id == id:
                return self.__teachers.pop(i)
        return None

    def listTeachers(
        self,
        query: Optional[str] = None,
        gender: Optional[Gender] = None,
        speciality: Optional[Speciality] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ) -> list[Teacher]:
        result = self.__teachers
        if query:
            result = [t for t in result if query.lower() in t.name.lower()]
        if gender:
            result = [t for t in result if t.gender == gender]
        if speciality:
            result = [t for t in result if t.speciality == speciality]

        if per_page is not None and page is not None and page > 0 and per_page > 0:
            start = (page - 1) * per_page
            end = start + per_page
            result = result[start:end]

        return result

    def getById(self, id: int) -> Optional[Teacher]:
        for teacher in self.__teachers:
            if teacher.id == id:
                return teacher
        return None

    def countTeachers(self) -> int:
        return len(self.__teachers)

    def countWithoutCourses(self, course_service) -> int:
        teachers_with_courses = {
            course.teacher_id
            for course in course_service.listCourses()
        }
        return sum(
            1 for t in self.__teachers
            if t.id not in teachers_with_courses
        )