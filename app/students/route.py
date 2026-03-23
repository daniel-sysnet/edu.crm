from math import ceil
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.student__service import student_service
from app.services.course__service import course_service
from app.services.activity__service import activity_service
from app.services.auth_service import auth_service
from app.models.genre import Genre
from app.models.action import Action
from app.auth.decorators import login_required

students_bp = Blueprint('students', __name__, url_prefix='/students')


@students_bp.route('/')
@login_required
def list():
    query = request.args.get('q')
    genre_param = request.args.get('genre')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    genre = Genre(genre_param) if genre_param else None
    students = student_service.listStudents(query=query, genre=genre)

    total = len(students)
    pages = ceil(total / per_page) if total > 0 else 1
    start = (page - 1) * per_page
    items = students[start:start + per_page]

    return render_template('students/list.html',
        items=items,
        total=total,
        page=page,
        pages=pages,
        per_page=per_page,
        query=query,
        genre=genre_param
    )


@students_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        from datetime import datetime
        name = request.form.get('name')
        email = request.form.get('email')
        genre = Genre(request.form.get('genre'))
        birthday = datetime.strptime(request.form.get('birthday'), '%Y-%m-%d').date()
        adresse = request.form.get('adresse')
        telephone = request.form.get('telephone')

        student = student_service.addStudent(
            name=name,
            email=email,
            genre=genre,
            birthday=birthday,
            adresse=adresse,
            telephone=telephone
        )

        user = auth_service.getUserById(session['user_id'])
        activity_service.log(
            action=Action.AJOUTER,
            model_type="Student",
            model_id=student.id,
            details=student.name,
            user=user
        )

        flash(f"Étudiant {student.name} ajouté avec succès", "success")
        return redirect(url_for('students.list'))

    return render_template('students/create.html')


@students_bp.route('/<int:id>')
@login_required
def detail(id: int):
    student = student_service.getById(id)
    if student is None:
        flash("Étudiant introuvable", "danger")
        return redirect(url_for('students.list'))

    courses = course_service.getCoursesByStudent(id)

    return render_template('students/detail.html',
        student=student,
        courses=courses
    )


@students_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id: int):
    student = student_service.deleteStudent(id)
    if student is None:
        flash("Étudiant introuvable", "danger")
        return redirect(url_for('students.list'))

    course_service.removeStudentFromAllCourses(id)

    user = auth_service.getUserById(session['user_id'])
    activity_service.log(
        action=Action.SUPPRIMER,
        model_type="Student",
        model_id=id,
        details=student.name,
        user=user
    )

    flash(f"Étudiant {student.name} supprimé avec succès", "success")
    return redirect(url_for('students.list'))


@students_bp.route('/<int:id>/assign', methods=['GET', 'POST'])
@login_required
def assign(id: int):
    student = student_service.getById(id)
    if student is None:
        flash("Étudiant introuvable", "danger")
        return redirect(url_for('students.list'))

    if request.method == 'POST':
        course_id = int(request.form.get('course_id'))
        course = course_service.assignStudent(course_id=course_id, student=student)
        if course is None:
            flash("Cours introuvable", "danger")
            return redirect(url_for('students.assign', id=id))

        flash(f"Étudiant affecté au cours {course.title} avec succès", "success")
        return redirect(url_for('students.detail', id=id))

    query = request.args.get('q')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    courses = course_service.listCourses(query=query)
    total = len(courses)
    pages = ceil(total / per_page) if total > 0 else 1
    start = (page - 1) * per_page
    items = courses[start:start + per_page]

    return render_template('students/assign.html',
        student=student,
        items=items,
        total=total,
        page=page,
        pages=pages,
        per_page=per_page,
        query=query
    )