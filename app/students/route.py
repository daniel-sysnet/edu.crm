from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.student__service import StudentService
from app.model.student import Student

students_bp = Blueprint('students', __name__, url_prefix='/students')
student_service = StudentService()


@students_bp.route('', methods=['GET'])
def list_students():
    students = student_service.list_students()
    return render_template('students/list.html', students=students)


@students_bp.route('/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        try:
            id = len(student_service.list_students()) + 1
            name = request.form.get('name')
            email = request.form.get('email')
            
            student = Student(id, name, email)
            student_service.add_student(student)
            flash(f'Étudiant "{name}" a bien été créé avec succès.', 'success')
            return redirect(url_for('students.list_students'))
        except ValueError as e:
            flash(f'Erreur lors de la création : {str(e)}', 'error')
            return render_template('students/create.html', error=str(e))
    
    return render_template('students/create.html')


@students_bp.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    deleted = student_service.delete_student(id)
    if deleted:
        flash('Étudiant supprimé avec succès.', 'success')
    else:
        flash('Erreur : l\'étudiant n\'a pas pu être supprimé.', 'error')
    return redirect(url_for('students.list_students'))
