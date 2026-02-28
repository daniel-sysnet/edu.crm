class Teacher:
    def __init__(self, id, name, email, speciality):
        self.__id = id
        self.__name = name
        self.__email = email
        self.__speciality = speciality

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def speciality(self):
        return self.__speciality

    @speciality.setter
    def speciality(self, value):
        self.__speciality = value