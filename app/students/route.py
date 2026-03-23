from math import ceil
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.student__service import StudentService
from app.models.gender import Gender
from app.models.action_type import ActionType
from app.auth.decorators import login_required

students_bp = Blueprint('students', __name__, url_prefix='/students')
student_service = StudentService()
# Services will be initialized as needed within route handlers


@students_bp.route('/')
@login_required
def list():
    query = request.args.get('q')
    gender_param = request.args.get('gender')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    gender = Gender(gender_param) if gender_param else None
    students = student_service.listStudents(query=query, gender=gender)

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
        gender=gender_param
    )


@students_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        from datetime import datetime
        name = request.form.get('name')
        email = request.form.get('email')
        gender = Gender(request.form.get('gender'))
        birthday = datetime.strptime(request.form.get('birthday'), '%Y-%m-%d').date()
        adresse = request.form.get('adresse')
        telephone = request.form.get('telephone')

        student = student_service.addStudent(
            name=name,
            email=email,
            gender=gender,
            birthday=birthday,
            adresse=adresse,
            telephone=telephone
        )

        # TODO: Uncomment when auth_service and activity_service are properly initialized
        # user = auth_service.getUserById(session['user_id'])
        # activity_service.log(
        #     action=ActionType.AJOUTER,
        #     model_type="Student",
        #     model_id=student.id,
        #     details=student.name,
        #     user=user
        # )

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

    # TODO: Uncomment when course_service is properly initialized
    # courses = course_service.getCoursesByStudent(id)

    return render_template('students/detail.html',
        student=student
        # courses=courses
    )


@students_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id: int):
    student = student_service.deleteStudent(id)
    if student is None:
        flash("Étudiant introuvable", "danger")
        return redirect(url_for('students.list'))

    # TODO: Uncomment when course_service is properly initialized
    # course_service.removeStudentFromAllCourses(id)

    # TODO: Uncomment when auth_service and activity_service are properly initialized
    # user = auth_service.getUserById(session['user_id'])
    # activity_service.log(
    #     action=ActionType.SUPPRIMER,
    #     model_type="Student",
    #     model_id=id,
    #     details=student.name,
    #     user=user
    # )

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