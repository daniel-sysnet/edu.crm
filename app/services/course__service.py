from typing import Optional, List
from app.extensions import db
from app.models.course import Course
from app.models.student import Student

class CourseService:
    def add_course(self, title: str, teacher_id: int) -> Course:
        """Crée un cours et génère son code unique[cite: 123, 219]."""
        new_course = Course(title=title, teacher_id=teacher_id)
        db.session.add(new_course)
        db.session.commit()
        return new_course

    def list_courses(self, query: str = None) -> List[Course]:
        """Retourne la liste filtrée par titre ou code[cite: 226, 238]."""
        if query:
            return Course.query.filter(
                (Course.title.ilike(f'%{query}%')) | 
                (Course.code.ilike(f'%{query}%'))
            ).all()
        return Course.query.all()

    def get_by_id(self, id: int) -> Optional[Course]:
        """Retourne un cours par son id[cite: 227]."""
        return Course.query.get(id)

    def get_by_code(self, code: str) -> Optional[Course]:
        """Récupère un cours par son code pour les routes[cite: 126]."""
        return Course.query.filter_by(code=code).first()

    def delete_course(self, id: int) -> bool:
        """Supprime un cours de la base[cite: 221]."""
        course = self.get_by_id(id)
        if course:
            db.session.delete(course)
            db.session.commit()
            return True
        return False

    def getCoursesByTeacher(self, teacher_id: int) -> List[Course]:
        """Retourne tous les cours d'un enseignant via SQL[cite: 228, 238]."""
        return Course.query.filter_by(teacher_id=teacher_id).all()

    def assign_student_to_course(self, course_id: int, student_id: int) -> bool:
        """Inscrit un étudiant (Many-to-Many)[cite: 136, 224]."""
        course = self.get_by_id(course_id)
        student = Student.query.get(student_id)
        if course and student and student not in course.students:
            course.students.append(student)
            db.session.commit()
            return True
        return False

    def countWithoutStudents(self) -> int:
        """Compte les cours sans aucun inscrit[cite: 235, 238]."""
        # On filtre les cours dont la relation 'students' est vide
        return Course.query.filter(~Course.students.any()).count()

    def get_most_popular(self) -> Optional[Course]:
        """Retourne le cours avec le plus d'étudiants[cite: 236, 238]."""
        courses = Course.query.all()
        return max(courses, key=lambda c: len(c.students)) if courses else None

    def count_courses(self) -> int:
        """Nombre total de cours[cite: 234]."""
        return Course.query.count()