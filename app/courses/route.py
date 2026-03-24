from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.services.course_service import CourseService

# Blueprint avec préfixe /courses comme imposé [cite: 127, 381]
courses_bp = Blueprint("courses", __name__, url_prefix="/courses")
course_service = CourseService()

@courses_bp.route("/")
def list():
    """Affiche la liste des cours avec recherche et pagination[cite: 66, 131]."""
    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("PAGINATION_DEFAULT", 8)

    all_results = course_service.list_courses(q)
    
    # Logique de pagination
    total = len(all_results)
    total_pages = max(1, -(-total // per_page))
    start = (page - 1) * per_page
    items = all_results[start:start + per_page]

    return render_template(
        "courses/list.html",
        courses=items,
        total=total,
        page=page,
        total_pages=total_pages,
        q=q
    )

@courses_bp.route("/create", methods=["GET", "POST"])
def create():
    """Formulaire et traitement de création[cite: 131, 382]."""
    from app.courses.forms import CourseForm
    form = CourseForm()
    
    if form.validate_on_submit():
        course_service.add_course(
            title=form.title.data,
            teacher_id=form.teacher_id.data
        )
        flash("Cours créé avec succès.", "success")
        return redirect(url_for("courses.list"))

    return render_template("courses/create.html", form=form)

@courses_bp.route("/<string:code>")
def detail(code):
    """Affiche le détail d'un cours via son code[cite: 131]."""
    course = course_service.get_by_code(code)
    if not course:
        flash("Cours introuvable.", "danger")
        return redirect(url_for("courses.list"))
    return render_template("courses/detail.html", course=course)

@courses_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    """Suppression sécurisée par ID[cite: 66, 131]."""
    if course_service.delete_course(id):
        flash("Le cours a été supprimé.", "success")
    else:
        flash("Erreur lors de la suppression.", "danger")
    return redirect(url_for("courses.list"))

@courses_bp.route("/<int:id>/assign", methods=["GET", "POST"])
def assign(id):
    """Inscription d'un étudiant au cours[cite: 131, 377]."""
    if request.method == "POST":
        student_id = request.form.get("student_id")
        if course_service.assign_student_to_course(id, student_id):
            flash("Étudiant inscrit au cours.", "success")
        else:
            flash("Erreur lors de l'inscription.", "danger")
        return redirect(url_for("courses.detail", code=course_service.get_by_id(id).code))
    
    course = course_service.get_by_id(id)
    return render_template("courses/assign.html", course=course)