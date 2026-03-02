from app.model.course import Course 

class CourseService:
    def __init__(self, student_service, teacher_service):
        self.courses = []
        self.student_service = student_service 
        self.teacher_service = teacher_service 

    def add_course(self, title: str, teacher_id: int) -> tuple:
        """Crée un objet Course après validation du professeur."""
        teachers = self.teacher_service.list_teachers()
        if not any(t.id == teacher_id for t in teachers):
            return None, "Erreur : Enseignant introuvable."

        new_course = Course(
            id=self.gen_id(),
            title=title,
            teacher_id=teacher_id,
            student_ids=[]
        )
        self.courses.append(new_course)
        return new_course, "Cours créé avec succès."

    def assign_student_to_course(self, course_id: int, student_id: int) -> tuple:
        """Ajoute un ID étudiant à la liste student_ids du cours[cite: 98]."""
        student = self.student_service.get_student_by_id(student_id)
        if not student:
            return False, "Étudiant introuvable."

        for course in self.courses:
            if course.id == course_id:
                if student_id not in course.student_ids:
                    course.student_ids.append(student_id)
                    return True, f"L'étudiant {student.name} inscrit au cours {course.title}."
                return False, "L'étudiant est déjà inscrit."
        
        return False, "Cours introuvable."

    def list_courses(self):
        return self.courses

    def delete_course(self, course_id: int) -> bool:
        for i, course in enumerate(self.courses):
            if course.id == course_id:
                self.courses.pop(i)
                return True
        return False

    def gen_id(self) -> int:
        return len(self.courses) + 1