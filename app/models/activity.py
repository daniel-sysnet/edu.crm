from datetime import datetime
from app.models.action import Action
from app.models.user import User


class Activity:
    counter: int = 0

    def __init__(self, action: Action, model_type: str, model_id: int, details: str, user: User):
        Activity.counter += 1
        self.__id = Activity.counter
        self.__createdAt = datetime.now()
        self.__action = action
        self.__model_type = model_type
        self.__model_id = model_id
        self.__details = details
        self.__user = user

    @property
    def id(self) -> int:
        return self.__id

    @property
    def createdAt(self) -> datetime:
        return self.__createdAt

    @property
    def action(self) -> Action:
        return self.__action

    @property
    def model_type(self) -> str:
        return self.__model_type

    @property
    def model_id(self) -> int:
        return self.__model_id

    @property
    def details(self) -> str:
        return self.__details

    @property
    def user(self) -> User:
        return self.__user