from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.auth.route import login_required

#  BLUEPRINT — Étudiant 2
# ══════════════════════════════════════════════════════════════════════════════
students_bp = Blueprint('students', __name__, url_prefix='/students')

# TODO Étudiant 2 : importer les fonctions du service
# from app.services.student_service import list_students, add_student, delete_student, get_student_by_id


# ── GET /students ─────────────────────────────────────────────────────────────
@students_bp.route('/')
@login_required
def list_students():
    # TODO Étudiant 2 : remplacer [] par list_students()
    students = []
    return render_template('students/list.html', students=students)


# ── GET / POST /students/create ───────────────────────────────────────────────
@students_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_student():
    if request.method == 'POST':
        # TODO Étudiant 2 : recuperer les champs du formulaire et appeler add_student()
        pass
    return render_template('students/create.html')


# ── GET /students/delete/<id> ─────────────────────────────────────────────────
@students_bp.route('/delete/<int:student_id>')
@login_required
def delete_student(student_id):
    # TODO Étudiant 2 : appeler delete_student(student_id)
    flash("Étudiant supprimé.", "success")
    return redirect(url_for('students.list_students'))