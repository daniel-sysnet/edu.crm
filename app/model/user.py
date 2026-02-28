class User:
    def __init__(self, id, login, password):
        self.__id = id
        self.__login = login
        self.__password = password

    @property
    def id(self):
        return self.__id

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, value):
        self.__login = value
        
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, value):
        self.__password = value
        