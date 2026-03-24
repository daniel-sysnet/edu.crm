from typing import Optional, List
from app.extensions import db
from app.models.course import Course
from app.models.student import Student

class CourseService:
    def add_course(self, title: str, teacher_id: int) -> Course:
        """Crée un cours et génère son code unique[cite: 97, 252]."""
        # 1. Création initiale
        new_course = Course(title=title, teacher_id=teacher_id)
        db.session.add(new_course)
        db.session.flush() # Pour obtenir l'ID avant le commit
        
        # 2. Génération du code métier (ex: CRS-001)
        new_course.code = Course.generate_code(new_course.id)
        db.session.commit()
        return new_course

    def list_courses(self, query: str = None) -> List[Course]:
        """Retourne la liste filtrée par titre ou code[cite: 99, 354, 366]."""
        if query:
            return Course.query.filter(
                (Course.title.ilike(f'%{query}%')) | 
                (Course.code.ilike(f'%{query}%'))
            ).all()
        return Course.query.all()

    def get_by_id(self, id: int) -> Optional[Course]:
        """Récupère un cours par sa clé primaire[cite: 355]."""
        return Course.query.get(id)

    def get_by_code(self, code: str) -> Optional[Course]:
        """Récupère un cours par son code (pour les URLs)[cite: 131]."""
        return Course.query.filter_by(code=code).first()

    def delete_course(self, id: int) -> bool:
        """Supprime un cours de la base[cite: 94, 349, 366]."""
        course = Course.query.get(id)
        if course:
            db.session.delete(course)
            db.session.commit()
            return True
        return False

    def assign_student_to_course(self, course_id: int, student_id: int) -> bool:
        """Inscrit un étudiant à un cours (Relation M:N)[cite: 98, 352, 366]."""
        course = Course.query.get(course_id)
        student = Student.query.get(student_id)
        if course and student:
            if student not in course.students:
                course.students.append(student)
                db.session.commit()
                return True
        return False

    def count_courses(self) -> int:
        """Nombre total de cours pour le Dashboard[cite: 112, 362]."""
        return Course.query.count()

    def get_most_popular(self) -> Optional[Course]:
        """Retourne le cours avec le plus d'étudiants[cite: 364, 366]."""
        courses = Course.query.all()
        if not courses: return None
        return max(courses, key=lambda c: len(c.students))