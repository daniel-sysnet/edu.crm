from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.course__service import CourseService
# On importe les instances déjà créées par tes camarades
from app.courses.route import student_service # Import depuis le fichier de l'étudiant 2
from app.teachers.route import teacher_service # Import depuis le fichier de l'étudiant 3
courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

# Ton service utilise maintenant les services des autres 
course_service = CourseService(student_service, teacher_service)

@courses_bp.route('/')
def list_courses():
    courses = course_service.list_courses()
    return render_template('courses/list.html', courses=courses)

@courses_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        t_id = int(request.form.get('teacher_id'))
        
        course, message = course_service.add_course(title, t_id)
        
        if course:
            flash(message, "success")
            return redirect(url_for('courses.list_courses'))
        else:
            flash(message, "danger")
    
    # Pour le formulaire, on envoie la liste des profs pour un <select>
    teachers = teacher_service.list_teachers()
    return render_template('courses/create.html', teachers=teachers)

@courses_bp.route('/assign', methods=['POST'])
def assign():
    c_id = int(request.form.get('course_id'))
    s_id = int(request.form.get('student_id'))
    
    success, message = course_service.assign_student_to_course(c_id, s_id)
    flash(message, "success" if success else "danger")
    return redirect(url_for('courses.list_courses'))

@courses_bp.route('/delete/<int:id>')
def delete(id):
    if course_service.delete_course(id):
        flash("Cours supprimé.", "info")
    else:
        flash("Erreur lors de la suppression.", "danger")
    return redirect(url_for('courses.list_courses'))