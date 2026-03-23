from datetime import datetime, date
from app.models.genre import Genre


class Student:
    counter: int = 0

    def __init__(self, name: str, email: str, genre: Genre, birthday: date, adresse: str, telephone: str):
        Student.counter += 1
        self.__id = Student.counter
        self.__name = name
        self.__email = email
        self.__genre = genre
        self.__birthday = birthday
        self.__adresse = adresse
        self.__telephone = telephone
        self.__createdAt = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        self.__email = value

    @property
    def genre(self) -> Genre:
        return self.__genre

    @property
    def birthday(self) -> date:
        return self.__birthday

    @property
    def adresse(self) -> str:
        return self.__adresse

    @adresse.setter
    def adresse(self, value: str) -> None:
        self.__adresse = value

    @property
    def telephone(self) -> str:
        return self.__telephone

    @telephone.setter
    def telephone(self, value: str) -> None:
        self.__telephone = value

    @property
    def createdAt(self) -> datetime:
        return self.__createdAt