from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.gender import Gender
from app.services.student__service import student_service
from app.utils.show_more import paginate_show_more
from app.auth.decorators import login_required

students_bp = Blueprint("students", __name__, url_prefix="/students")

@students_bp.route("/")
@login_required
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
@login_required
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
@login_required
def detail(mat):
    """Affiche le détail via le matricule."""
    student = student_service.getByMatricule(mat)
    if not student:
        flash("Étudiant introuvable", "danger")
        return redirect(url_for("students.list"))

    # Cours triés du plus récent au plus ancien
    all_courses = sorted(student.courses, key=lambda c: c.created_at, reverse=True)

    result = paginate_show_more(
        items   = all_courses,
        more    = request.args.get("more", 0, type=int),
        initial = current_app.config.get("PROFILE_LIST_INITIAL", 5),
        steps   = current_app.config.get("PROFILE_LIST_STEPS", [10, 20, -1]),
    )

    return render_template(
        "students/detail.html",
        student       = student,
        courses       = result["items"],
        total_courses = result["total"],
        has_more      = result["has_more"],
        next_more     = result["next_more"],
    )

@students_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
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