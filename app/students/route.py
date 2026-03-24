from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
# On garde le nom exact de ton fichier service
from app.services.student__service import student_service 
from app.models.gender import Gender

students_bp = Blueprint("students", __name__, url_prefix="/students")

@students_bp.route("/")
def list():
    q = request.args.get("q", "").strip()
    gender = request.args.get("gender", "")
    page = request.args.get("page", 1, type=int)
    
    # Pagination dynamique
    default_per_page = current_app.config.get("PAGINATION_DEFAULT", 10)
    per_page = request.args.get("per_page", default_per_page, type=int)

    # Conversion pour le filtrage
    gender_enum = None
    if gender in ["M", "F"]:
        gender_enum = Gender[gender]

    all_filtered = student_service.listStudents(q, gender_enum)

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
    """Cette fonction manquait, c'est elle qui causait l'erreur 500 sur l'index."""
    from app.students.form import StudentForm
    form = StudentForm()

    if form.validate_on_submit():
        student_service.addStudent(
            name=form.name.data,
            email=form.email.data,
            genre=form.gender.data,
            birthday=form.dob.data,
            adresse=form.address.data,
            telephone=form.phone.data
        )
        flash("Étudiant inscrit avec succès.", "success")
        return redirect(url_for("students.list"))

    return render_template("students/create.html", form=form)

@students_bp.route("/<string:mat>")
def detail(mat):
    """Affiche le détail via le matricule."""
    student = student_service.getByMatricule(mat)
    if not student:
        flash("Étudiant introuvable", "danger")
        return redirect(url_for("students.list"))
    return render_template("students/detail.html", student=student)

@students_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    """Supprime un étudiant par son ID en base de données."""
    from app.extensions import db
    from app.models.student import Student
    student = Student.query.get(id)

    if student:
        db.session.delete(student)
        db.session.commit()
        flash(f"L'étudiant {student.name} a été supprimé avec succès.", "success")
    else:
        flash("Erreur : Étudiant introuvable.", "danger")
        
    return redirect(url_for("students.list"))