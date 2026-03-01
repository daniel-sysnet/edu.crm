from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.teacher_service import TeacherService
from app.model.teacher import Teacher
from app.model.speciality import Speciality

# Déclaration du Blueprint
teachers_bp = Blueprint(
    "teachers",                        
    __name__,
    template_folder="../../templates/teachers",
    url_prefix="/teachers",
)

teacher_service = TeacherService()


# Route 1 : Liste des enseignants
@teachers_bp.route("/")
def list():
    """Affiche la liste complète des enseignants."""
    all_teachers = teacher_service.list_teachers()
    return render_template("teachers/list.html", teachers=all_teachers)

# Route 2 : Ajout d'un enseignant
@teachers_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name       = request.form.get("name", "").strip()
        email      = request.form.get("email", "").strip()
        speciality = request.form.get("speciality", "").strip()
        if not name or not email or not speciality:
            flash("Tous les champs sont obligatoires.", "danger")
            return render_template("teachers/create.html")
        try:
            fspeciality = Speciality.from_string(speciality)
            teacher_service.add_teacher(name=name, email=email, speciality=fspeciality)
            flash(f"Enseignant '{name}' ajouté avec succès.", "success")
            return redirect(url_for("teachers.list"))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("teachers/create.html")
    return render_template("teachers/create.html")

# Route 3 : Suppression d'un enseignant
@teachers_bp.route("/delete/<int:teacher_id>")
def delete(teacher_id: int):
    """Supprime un enseignant par son id."""
    deleted = teacher_service.delete_teacher(teacher_id)

    if deleted:
        flash("Enseignant supprimé avec succès.", "success")
    else:
        flash("Enseignant introuvable.", "warning")

    return redirect(url_for("teachers.list"))