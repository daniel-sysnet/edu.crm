from datetime import datetime


class User:
    counter: int = 0

    def __init__(self, login: str, password: str, name: str):
        User.counter += 1
        self.__id: int = User.counter
        self.__login: str = login
        self.__password: str = password
        self.__name: str = name
        self.__createdAt: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def login(self) -> str:
        return self.__login

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str) -> None:
        self.__password = value

    @property
    def createdAt(self) -> datetime:
        return self.__createdAt