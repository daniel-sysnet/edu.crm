from app.model.teacher import Teacher
from app.model.speciality import Speciality

class TeacherService:
    """Service pour gérer les enseignants."""

    def __init__(self):
        self.teachers = []

    def list_teachers(self):
        """Retourne la liste de tous les enseignants."""
        return self.teachers

    def add_teacher(self,name: str, email: str, speciality: Speciality) -> None:
        """Ajoute un nouvel enseignant."""
        teacher = Teacher(name=name, email=email, speciality=speciality, id=self.gen_id())
        self.teachers.append(teacher)

    def delete_teacher(self, teacher_id: int) -> bool:
        """Supprime un enseignant par son id."""
        for i, teacher in enumerate(self.teachers):
            if teacher.id == teacher_id:
                self.teachers.pop(i)
                return True
        return False
    
    def gen_id(self) -> int:
        """Génère un ID unique pour un nouvel enseignant."""
        return len(self.teachers) + 1