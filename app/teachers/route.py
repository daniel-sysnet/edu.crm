from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.auth.route import login_required

# ══════════════════════════════════════════════════════════════════════════════
#  BLUEPRINT — Étudiant 3
# ══════════════════════════════════════════════════════════════════════════════
teachers_bp = Blueprint('teachers', __name__, url_prefix='/teachers')

# TODO Étudiant 3 : importer les fonctions du service
# from app.services.teacher_service import list_teachers, add_teacher, delete_teacher


# ── GET /teachers ─────────────────────────────────────────────────────────────
@teachers_bp.route('/')
@login_required
def list_teachers():
    # TODO Étudiant 3 : remplacer [] par list_teachers()
    teachers = []
    return render_template('teachers/list.html', teachers=teachers)


# ── GET / POST /teachers/create ───────────────────────────────────────────────
@teachers_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_teacher():
    if request.method == 'POST':
        # TODO Étudiant 3 : récupérer les champs (name, email, speciality) et appeler add_teacher()
        pass
    return render_template('teachers/create.html')


# ── GET /teachers/delete/<id> ─────────────────────────────────────────────────
@teachers_bp.route('/delete/<int:teacher_id>')
@login_required
def delete_teacher(teacher_id):
    # TODO Étudiant 3 : appeler delete_teacher(teacher_id)
    flash("Enseignant supprimé.", "success")
    return redirect(url_for('teachers.list_teachers'))