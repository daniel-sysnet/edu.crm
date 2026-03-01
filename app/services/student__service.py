from app.model.student import Student


class StudentService:
    def __init__(self):
        self.students = []
    
    def add_student(self, name: str, email: str) -> None:
        id = self.gen_id()
        student = Student(id, name, email)
        self.students.append(student)
    
    def delete_student(self, student_id: int) -> bool:
        for i, student in enumerate(self.students):
            if student.id == student_id:
                self.students.pop(i)
                return True
        return False
    
    def list_students(self) -> list:
        return self.students
    
    def get_student_by_id(self, student_id: int) -> Student:
        
        for student in self.students:
            if student.id == student_id:
                return student
        return None
    
    def gen_id(self)->int:
        return len(self.students) + 1
