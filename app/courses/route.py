from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.course__service import CourseService
from app.students.route import student_service 
from app.teachers.route import teacher_service 

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')
course_service = CourseService()

@courses_bp.route('/')
def list():
    query = request.args.get('query')
    courses = course_service.listCourses(query)
    return render_template('courses/list.html', courses=courses)

@courses_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        teacher_id = request.form.get('teacher_id')
        
        teacher = teacher_service.getById(int(teacher_id)) if teacher_id else None
        
        if title and teacher:
            course_service.addCourse(title, teacher)
            flash("Cours créé avec succès.", "success")
            return redirect(url_for('courses.list'))
        
        flash("Erreur : Titre ou Enseignant invalide.", "danger")
    
    teachers = teacher_service.listTeachers()
    return render_template('courses/create.html', teachers=teachers)

@courses_bp.route('/<int:id>')
def detail(id):
    course = course_service.getById(id)
    if not course:
        flash("Cours introuvable.", "danger")
        return redirect(url_for('courses.list'))
    return render_template('courses/detail.html', course=course)

@courses_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if course_service.deleteCourse(id):
        flash("Cours supprimé.", "success")
    else:
        flash("Erreur lors de la suppression.", "danger")
    return redirect(url_for('courses.list'))

@courses_bp.route('/<int:id>/assign', methods=['GET', 'POST'])
def assign(id):
    course = course_service.getById(id)
    if not course:
        flash("Cours introuvable.", "danger")
        return redirect(url_for('courses.list'))

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        student = student_service.getById(int(student_id)) if student_id else None
        
        if student and course_service.assignStudent(id, student):
            flash(f"Étudiant {student.name} inscrit.", "success")
            return redirect(url_for('courses.detail', id=id))
        flash("Erreur lors de l'inscription.", "danger")

    students = student_service.listStudents()
    return render_template('courses/assign.html', course=course, students=students)