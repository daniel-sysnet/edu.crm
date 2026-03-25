from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.services.course__service import CourseService
from app.services.student__service import student_service
from app.utils.show_more import paginate_show_more

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")
course_service = CourseService()


@courses_bp.route("/")
def list():
    """Liste les cours."""
    q        = request.args.get("q", "").strip()
    page     = request.args.get("page", 1, type=int)
    per_page = request.args.get(
        "per_page",
        current_app.config.get("PAGINATION_DEFAULT", 5),
        type=int,
    )

    all_results = course_service.list_courses(q)

    total       = len(all_results)
    total_pages = max(1, -(-total // per_page))
    start       = (page - 1) * per_page
    items       = all_results[start:start + per_page]

    return render_template(
        "courses/list.html",
        courses     = items,
        total       = total,
        per_page    = per_page,
        page        = page,
        total_pages = total_pages,
        q           = q,
    )


@courses_bp.route("/create", methods=["GET", "POST"])
def create():
    from app.courses.form import CourseForm
    from app.services.teacher_service import TeacherService

    form           = CourseForm()
    teacher_service = TeacherService()

    # Recherche enseignant par matricule
    teacher_search = (
        request.args.get("teacher_search") or
        request.form.get("teacher_search") or ""
    ).strip()
    teacher_found = None
    if teacher_search:
        teacher_found = teacher_service.getByMatricule(teacher_search)

    if teacher_found:
        form.teacher_id.data = str(teacher_found.id)

    if form.validate_on_submit():
        course_service.add_course(
            title      = form.title.data,
            teacher_id = form.teacher_id.data,
        )
        flash("Cours créé avec succès.", "success")
        return redirect(url_for("courses.list"))

    return render_template(
        "courses/create.html",
        form           = form,
        teacher_search = teacher_search,
        teacher_found  = teacher_found,
    )


@courses_bp.route("/<string:code>")
def detail(code):
    course = course_service.get_by_code(code)
    if not course:
        flash("Cours introuvable.", "danger")
        return redirect(url_for("courses.list"))

    # Étudiants triés du plus récent au plus ancien
    all_students = sorted(course.students, key=lambda s: s.created_at, reverse=True)

    # Pagination progressive (utilitaire réutilisable)
    result = paginate_show_more(
        items   = all_students,
        more    = request.args.get("more", 0, type=int),
        initial = current_app.config.get("PROFILE_LIST_INITIAL", 5),
        steps   = current_app.config.get("PROFILE_LIST_STEPS", [10, 20, -1]),
    )

    return render_template(
        "courses/detail.html",
        course         = course,
        students       = result["items"],
        total_students = result["total"],
        has_more       = result["has_more"],
        next_more      = result["next_more"],
    )


@courses_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    """Suppression d'un cours."""
    if course_service.delete_course(id):
        flash("Le cours a été supprimé.", "success")
    else:
        flash("Erreur lors de la suppression.", "danger")
    return redirect(url_for("courses.list"))


@courses_bp.route("/<string:code>/assign", methods=["GET", "POST"])
def assign(code):
    """Inscription/affectation d'un étudiant au cours."""
    course = course_service.get_by_code(code)
    if not course:
        flash("Cours introuvable.", "danger")
        return redirect(url_for("courses.list"))
    
    if request.method == "POST":
        student_id = request.form.get("student_id", type=int)
        if course_service.assign_student_to_course(course.id, student_id):
            flash("Étudiant inscrit au cours.", "success")
        else:
            flash("Erreur lors de l'inscription.", "danger")
        # Rediriger avec les mêmes paramètres de filtre
        return redirect(url_for("courses.assign", code=code, **request.args))

    # ── Filtrage & pagination des étudiants ──
    q        = request.args.get("q", "").strip()
    page     = request.args.get("page", 1, type=int)
    per_page = request.args.get(
        "per_page",
        current_app.config.get("PAGINATION_DEFAULT", 5),
        type=int,
    )

    all_students = student_service.listStudents(query=q if q else None)

    total       = len(all_students)
    total_pages = max(1, -(-total // per_page))
    page        = max(1, min(page, total_pages))
    start       = (page - 1) * per_page
    items       = all_students[start:start + per_page]

    # IDs des étudiants déjà inscrits à ce cours
    enrolled_ids = {s.id for s in course.students}

    return render_template(
        "courses/assign.html",
        course       = course,
        students     = items,
        enrolled_ids = enrolled_ids,
        total        = total,
        page         = page,
        per_page     = per_page,
        total_pages  = total_pages,
        q            = q,
    )
    return render_template("courses/assign.html", course=course)

@courses_bp.route("/<string:code>/unassign/<int:student_id>", methods=["POST"])
def unassign(code, student_id):
    """Désinscrit un étudiant d'un cours via son code."""
    course = course_service.get_by_code(code)
    if not course:
        flash("Cours introuvable.", "danger")
        return redirect(url_for("courses.list"))

    if course_service.unassign_student_to_course(course.id, student_id):
        flash("L'étudiant a été retiré du cours.", "success")
    else:
        flash("Erreur lors de la désinscription.", "danger")

    # Revenir à la page d'origine (assign ou detail)
    next_url = request.args.get("next") or url_for("courses.detail", code=code)
    return redirect(next_url)