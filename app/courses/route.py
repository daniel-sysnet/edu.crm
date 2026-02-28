from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.auth.route import login_required

# ══════════════════════════════════════════════════════════════════════════════
#  BLUEPRINT — Étudiant 4
# ══════════════════════════════════════════════════════════════════════════════
courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

# TODO Étudiant 4 : importer les fonctions du service
# from app.services.course_service import list_courses, add_course, assign_student_to_course


# ── GET /courses ──────────────────────────────────────────────────────────────
@courses_bp.route('/')
@login_required
def list_courses():
    # TODO Étudiant 4 : remplacer [] par list_courses()
    courses = []
    return render_template('courses/list.html', courses=courses)


# ── GET / POST /courses/create ────────────────────────────────────────────────
@courses_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_course():
    if request.method == 'POST':
        # TODO Étudiant 4 : récupérer les champs (title, teacher_id) et appeler add_course()
        pass
    return render_template('courses/create.html')


# ── GET /courses/delete/<id> ──────────────────────────────────────────────────
@courses_bp.route('/delete/<int:course_id>')
@login_required
def delete_course(course_id):
    # TODO Étudiant 4 : appeler delete_course(course_id)
    flash("Cours supprimé.", "success")
    return redirect(url_for('courses.list_courses'))