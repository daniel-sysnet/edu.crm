class Student:
    def __init__(self, id: int, name: str, email: str):
        self.__id = id
        self.__name = name
        self.__email = email
        
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Le nom ne peut pas être vide")
        self.__name = value
        
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Email invalide")
        self.__email = value