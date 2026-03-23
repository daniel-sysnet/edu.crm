from typing import Optional, List
from app.model.course import Course
from app.model.teacher import Teacher
from app.model.student import Student

class CourseService:
    def __init__(self):
        self.courses: List[Course] = []

    def addCourse(self, title: str, teacher: Teacher) -> Course:
        new_course = Course(title=title, teacher=teacher)
        self.courses.append(new_course)
        return new_course

    def deleteCourse(self, id: int) -> Optional[Course]:
        course = self.getById(id)
        if course:
            self.courses.remove(course)
            return course
        return None

    def assignStudent(self, course_id: int, student: Student) -> Optional[Course]:
        course = self.getById(course_id)
        if course and student.id not in course.students_ids:
            course.addStudent(student)
            return course
        return None

    def getById(self, id: int) -> Optional[Course]:
        return next((c for c in self.courses if c.id == id), None)

    def listCourses(self, query: str = None) -> List[Course]:
        if query:
            return [c for c in self.courses if query.lower() in c.title.lower()]
        return self.courses

    def countCourses(self) -> int:
        return len(self.courses)