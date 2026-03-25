from datetime import date
from typing import Optional
from app.models.student import Student
from app.models.gender import Genre


class StudentService:
    def __init__(self):
        self.__students: list[Student] = []
        self.__next_id = 1

    def addStudent(self, name: str, email: str, genre: Genre, birthday: date, adresse: str, telephone: str) -> Student:
        student = Student(
            id=self.__next_id,
            name=name,
            email=email,
            genre=genre,
            birthday=birthday,
            adresse=adresse,
            telephone=telephone
        )
        self.__students.append(student)
        self.__next_id += 1
        return student

    def deleteStudent(self, matricule: str) -> Optional[Student]:
        student = self.getByMatricule(matricule)
        if student is None:
            return None
        self.__students.remove(student)
        return student

    def updateStudent(self, matricule: str, name: str, email: str, genre: Genre, birthday: date, adresse: str, telephone: str) -> Optional[Student]:
        student = self.getByMatricule(matricule)
        if student is None:
            return None

        student.name = name
        student.email = email
        student.genre = genre
        student.birthday = birthday
        student.adresse = adresse
        student.telephone = telephone

        return student

    def listStudents(self, query: str = None, genre: Genre = None) -> list[Student]:
        result = self.__students

        if query:
            result = [s for s in result if
                query.lower() in s.name.lower() or
                query.lower() in s.email.lower() or
                query.lower() in s.matricule.lower()
            ]

        if genre:
            result = [s for s in result if s.genre == genre]

        return result

    def getByMatricule(self, matricule: str) -> Optional[Student]:
        for student in self.__students:
            if student.matricule == matricule:
                return student
        return None

    def countStudents(self) -> int:
        return len(self.__students)


student_service = StudentService()