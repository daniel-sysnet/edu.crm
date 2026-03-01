class CourseService:
    def __init__(self, student_service, teacher_service):
        self.courses = []
        self.student_service = student_service  
        self.teacher_service = teacher_service 

    def add_course(self, title, teacher_id):
        teachers = self.teacher_service.list_teachers()
        if not any(t.id == teacher_id for t in teachers):
            return None, "Erreur : Enseignant introuvable."

        new_id = len(self.courses) + 1
        course = {
            'id': new_id,
            'title': title,
            'teacher_id': teacher_id,
            'student_ids': []
        }
        self.courses.append(course)
        return course, "Cours créé avec succès."

    def assign_student_to_course(self, course_id, student_id):
        student = self.student_service.get_student_by_id(student_id)
        if not student:
            return False, "Étudiant introuvable."

        for course in self.courses:
            if course['id'] == course_id:
                if student_id not in course['student_ids']:
                    course['student_ids'].append(student_id)
                    return True, f"L'étudiant {student.name} a été ajouté au cours."
                return False, "L'étudiant est déjà inscrit à ce cours."
        
        return False, "Cours introuvable."

    def list_courses(self):
        return self.courses

    def delete_course(self, course_id):
        initial_len = len(self.courses)
        self.courses = [c for c in self.courses if c['id'] != course_id]
        return len(self.courses) < initial_len