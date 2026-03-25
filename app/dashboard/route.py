from flask import Blueprint, render_template
from app.auth.decorators import login_required
from app.services.student__service import student_service
from app.services.course__service import course_service
from app.services.teacher_service import teacher_service

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/")


# ── Routes ────────────────────────────────────────────────────────────────────

@dashboard_bp.route("/")
@login_required
def index():
    # Calculer les stats à partir des services
    total_students = student_service.countStudents()
    total_teachers = teacher_service.countTeachers()
    total_courses = course_service.count_courses()
    courses_empty = course_service.countWithoutStudents()
    most_popular = course_service.get_most_popular()
    most_popular_course = most_popular.title if most_popular else "N/A"
    total_enrolled = student_service.countEnrolled()
    students_no_course = student_service.countWithoutCourses()
    active_teachers = teacher_service.countActive()
    
    stats = {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_courses": total_courses,
        "courses_empty": courses_empty,
        "most_popular_course": most_popular_course,
        "total_enrolled": total_enrolled,
        "students_no_course": students_no_course,
        "active_teachers": active_teachers,
    }
    
    return render_template(
        "dashboard/index.html",
        stats = stats
    )