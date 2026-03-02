from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.course__service import CourseService
from app.students.route import student_service 
from app.teachers.route import teacher_service 

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')
course_service = CourseService(student_service, teacher_service)

@courses_bp.route('/')
def list_courses():
    courses = course_service.list_courses()
    return render_template('courses/list.html', courses=courses)

@courses_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        try:
            t_id = int(request.form.get('teacher_id'))
            course, message = course_service.add_course(title, t_id)
            
            if course:
                flash(message, "success")
                return redirect(url_for('courses.list_courses'))
            else:
                flash(message, "danger")
        except ValueError:
            flash("L'ID de l'enseignant doit être un nombre.", "danger")
    
    teachers = teacher_service.list_teachers()
    return render_template('courses/create.html', teachers=teachers)

@courses_bp.route('/delete/<int:id>')
def delete(id):
    if course_service.delete_course(id):
        flash(f"Cours {id} supprimé.", "info")
    else:
        flash("Erreur : cours introuvable.", "danger")
    return redirect(url_for('courses.list_courses'))