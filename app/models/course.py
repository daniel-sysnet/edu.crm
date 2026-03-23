from datetime import datetime
from app.models.teacher import Teacher
from app.models.student import Student


class Course:
    counter: int = 0

    def __init__(self, title: str, teacher: Teacher):
        Course.counter += 1
        self.__id = Course.counter
        self.__title = title
        self.__teacher_id = teacher.id
        self.__students_ids = []
        self.__teacher = teacher
        self.__students = []
        self.__createdAt = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        self.__title = value

    @property
    def teacher_id(self) -> int:
        return self.__teacher_id

    @property
    def students_ids(self) -> list[int]:
        return self.__students_ids

    @property
    def teacher(self) -> Teacher:
        return self.__teacher

    @teacher.setter
    def teacher(self, value: Teacher) -> None:
        self.__teacher = value
        self.__teacher_id = value.id

    @property
    def students(self) -> list[Student]:
        return self.__students

    @property
    def createdAt(self) -> datetime:
        return self.__createdAt

    def addStudent(self, student: Student) -> None:
        self.__students_ids.append(student.id)
        self.__students.append(student)