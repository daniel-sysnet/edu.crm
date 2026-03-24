from datetime import date
from typing import Optional
from app.models.student import Student
from app.models.genre import Genre


class StudentService:
    def __init__(self):
        self.__students: list[Student] = []

    def addStudent(self, name: str, email: str, genre: Genre, birthday: date, adresse: str, telephone: str) -> Student:
        student = Student(
            name=name,
            email=email,
            genre=genre,
            birthday=birthday,
            adresse=adresse,
            telephone=telephone
        )
        self.__students.append(student)
        return student

    def deleteStudent(self, id: int) -> Optional[Student]:
        student = self.getById(id)
        if student is None:
            return None
        self.__students.remove(student)
        return student

    def listStudents(self, query: str = None, genre: Genre = None) -> list[Student]:
        result = self.__students
        if query:
            result = [s for s in result if
                query.lower() in s.name.lower() or
                query.lower() in s.email.lower()
            ]
        if genre:
            result = [s for s in result if s.genre == genre]
        return result

    def getById(self, id: int) -> Optional[Student]:
        for student in self.__students:
            if student.id == id:
                return student
        return None

    def countStudents(self) -> int:
        return len(self.__students)


student_service = StudentService()