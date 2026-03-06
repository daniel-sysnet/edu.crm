from typing import Optional, List
from app.models.course import Course 

class CourseService:
    def __init__(self, student_service, teacher_service):
        self.courses = []
        self.student_service = student_service 
        self.teacher_service = teacher_service 

    def add_course(self, title: str, teacher_id: int) -> Optional[Course]:
        teacher = self.teacher_service.get_teacher_by_id(teacher_id)
        if not teacher:
            return None

        new_course = Course(
            id=self.gen_id(),
            title=title,
            teacher_id=teacher_id,
            student_ids=[]
        )
        self.courses.append(new_course)
        return new_course

    def assign_student_to_course(self, course_id: int, student_id: int) -> bool:
        student = self.student_service.get_student_by_id(student_id)
        if not student:
            return False

        course = self.get_course_by_id(course_id)
        if course and student_id not in course.student_ids:
            course.student_ids.append(student_id)
            return True
        
        return False

    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        return next((c for c in self.courses if c.id == course_id), None)

    def list_courses(self) -> List[Course]:
        return self.courses

    def delete_course(self, course_id: int) -> bool:
        course = self.get_course_by_id(course_id)
        if course:
            self.courses.remove(course)
            return True
        return False

    def gen_id(self) -> int:
        return len(self.courses) + 1