from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.services.student__service import student_service
from app.models.gender import Genre

students_bp = Blueprint("students", __name__, url_prefix="/students")

@students_bp.route("/")
def list():
    """Liste les étudiants avec filtres et pagination[cite: 249]."""
    q = request.args.get("q", "").strip()
    gender = request.args.get("gender", "")
    page = request.args.get("page", 1, type=int)
    
    # Pagination dynamique corrigée
    default_per_page = current_app.config.get("PAGINATION_DEFAULT", 10)
    per_page = request.args.get("per_page", default_per_page, type=int)

    genre_enum = Genre[gender] if gender in [g.name for g in Genre] else None

    all_filtered = student_service.listStudents(q, genre_enum)

    # Logique de découpage (Slicing)
    total = len(all_filtered)
    total_pages = max(1, -(-total // per_page))
    start = (page - 1) * per_page
    items = all_filtered[start:start + per_page]

    return render_template(
        "students/list.html",
        students=items,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        q=q,
        gender=gender
    )

@students_bp.route("/create", methods=["GET", "POST"])
def create():
    """Formulaire et traitement d'ajout."""
    from app.students.form import StudentForm
    form = StudentForm()

    if form.validate_on_submit():
        student_service.addStudent(
            name=form.name.data,
            email=form.email.data,
            genre=form.genre.data, # Directement l'Enum si le formulaire est bien fait
            birthday=form.birthday.data,
            adresse=form.adresse.data,
            telephone=form.telephone.data
        )
        flash("Étudiant ajouté avec succès.", "success")
        return redirect(url_for("students.list"))

    return render_template("students/create.html", form=form)

@students_bp.route("/<int:id>")
def detail(id):
    """Profil détaillé de l'étudiant."""
    student = student_service.getById(id)
    if not student:
        flash("Étudiant introuvable", "danger")
        return redirect(url_for("students.list"))
    return render_template("students/detail.html", student=student)

@students_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    """Suppression d'un étudiant."""
    if student_service.deleteStudent(id):
        flash("Étudiant supprimé avec succès", "success")
    else:
        flash("Erreur lors de la suppression", "danger")
    return redirect(url_for("students.list"))