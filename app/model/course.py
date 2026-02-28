class Course:
    def __init__(self, id, title, teacher_id):
        self.__id = id
        self.__title = title
        self.__teacher_id = teacher_id
        self.__students_ids = []

    
    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if len(value) < 2:
            raise ValueError("Titre trop court")
        self.__title = value
        
    @property
    def teacher_id(self):
        return self.__teacher_id

    @property
    def students_ids(self):
        return self.__students_ids
    
    def add_student(self, student_id):
        if student_id not in self.__students_ids:
            self.__students_ids.append(student_id)