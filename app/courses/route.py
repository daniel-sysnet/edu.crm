from flask import Blueprint, render_template, request

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


# ── Données statiques de test ───────────────────────────────────────────────── (supprimer après implémentation service Alchemy)

COURSES = [
    {
        "id": 1, "code": "CRS-101",
        "title": "Introduction au Design UX",
        "teacher": {"id": 2, "matricule": "ENS-002", "name": "Sylvie Laurent",   "photo_url": ""},
        "student_count": 18,
    },
    {
        "id": 2, "code": "CRS-102",
        "title": "Analyse de Données avec Python",
        "teacher": {"id": 1, "matricule": "ENS-001", "name": "Marc Tremblay",    "photo_url": ""},
        "student_count": 24,
    },
    {
        "id": 3, "code": "CRS-103",
        "title": "Réseaux Informatiques Avancés",
        "teacher": {"id": 3, "matricule": "ENS-003", "name": "Alain Martin",     "photo_url": ""},
        "student_count": 15,
    },
    {
        "id": 4, "code": "CRS-104",
        "title": "Machine Learning Fondamental",
        "teacher": {"id": 4, "matricule": "ENS-004", "name": "Isabelle Richard", "photo_url": ""},
        "student_count": 30,
    },
    {
        "id": 5, "code": "CRS-105",
        "title": "Développement Front-End avec React",
        "teacher": {"id": 5, "matricule": "ENS-005", "name": "Robert Dupont",    "photo_url": ""},
        "student_count": 22,
    },
    {
        "id": 6, "code": "CRS-106",
        "title": "Bases de Données Avancées",
        "teacher": {"id": 1, "matricule": "ENS-001", "name": "Marc Tremblay",    "photo_url": ""},
        "student_count": 20,
    },
    {
        "id": 7, "code": "CRS-107",
        "title": "Sécurité Informatique",
        "teacher": {"id": 3, "matricule": "ENS-003", "name": "Alain Martin",     "photo_url": ""},
        "student_count": 12,
    },
    {
        "id": 8, "code": "CRS-108",
        "title": "Intelligence Artificielle Appliquée",
        "teacher": {"id": 4, "matricule": "ENS-004", "name": "Isabelle Richard", "photo_url": ""},
        "student_count": 28,
    },
]


# ── Routes ────────────────────────────────────────────────────────────────────

@courses_bp.route("/")
def list():
    from flask import current_app

    q        = request.args.get("q", "").strip().lower()
    per_page = int(request.args.get("per_page", current_app.config["PAGINATION_DEFAULT"]))
    page     = int(request.args.get("page", 1))

    # Utiliser le service avec Alchemy ici (remplacer)
    # --- Filtrage statique ---
    filtered = COURSES

    if q:
        filtered = [
            c for c in filtered
            if q in c["title"].lower()
            or q in c["code"].lower()
        ]
    # --- fin filtrage statique ---

    total       = len(filtered)
    total_pages = max(1, -(-total // per_page))
    page        = max(1, min(page, total_pages))
    start       = (page - 1) * per_page
    items       = filtered[start:start + per_page]

    return render_template(
        "courses/list.html",
        courses     = items,
        total       = total,
        page        = page,
        per_page    = per_page,
        total_pages = total_pages,
        q           = q,
        admin= {"name": "Jean Dupont", "photo_url": ""},
    )


@courses_bp.route("/create", methods=["GET", "POST"])
def create():
    from app.courses.forms import CourseForm
    from flask import current_app, flash, redirect
    form = CourseForm()
    teacher_search = request.args.get("teacher_search", "").strip().upper()
    teacher_found  = None

    # Utiliser le service avec Alchemy ici (remplacer)
    # --- Recherche statique enseignant par matricule ---
    if teacher_search:
        from app.teachers.routes import TEACHERS
        teacher_found = next(
            (t for t in TEACHERS if t["matricule"] == teacher_search), None
        )
        if teacher_found and request.method == "GET":
            form.teacher_id.data = str(teacher_found["id"])
    # --- fin recherche statique ---

    if form.validate_on_submit():
        # TODO: course_service.add_course()
        flash("Cours créé avec succès.", "success")
        return redirect(url_for("courses.list"))

    return render_template(
        "courses/create.html",
        form           = form,
        teacher_search = teacher_search,
        teacher_found  = teacher_found,
        current_user   = {"name": "Jean Dupont", "photo_url": ""},
    )


@courses_bp.route("/<str:code>")
def detail(code):
    return render_template("courses/detail.html")


@courses_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    return render_template("courses/edit.html")


@courses_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    pass


@courses_bp.route("/<int:id>/enroll", methods=["POST"])
def enroll(id):
    pass