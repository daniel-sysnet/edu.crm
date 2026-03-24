from flask import Blueprint, render_template, request, url_for
from app.models.gender import Gender

students_bp = Blueprint("students", __name__, url_prefix="/students")


# ── Données statiques de test ─────────────────────────────────────────────────

STUDENTS = [
    {"id": 1, "matricule": "STU-001", "name": "Lucas Bernard",   "email": "lucas.bernard@edu.crm",  "phone": "771234567", "gender": Gender.M, "photo_url": ""},
    {"id": 2, "matricule": "STU-002", "name": "Emma Morel",      "email": "emma.morel@edu.crm",      "phone": "789876543", "gender": Gender.F, "photo_url": ""},
    {"id": 3, "matricule": "STU-003", "name": "Julien Petit",    "email": "julien.petit@edu.crm",    "phone": "764512890", "gender": Gender.M, "photo_url": ""},
    {"id": 4, "matricule": "STU-004", "name": "Sophie Lefebvre", "email": "sophie.l@edu.crm",        "phone": "703322110", "gender": Gender.F, "photo_url": ""},
    {"id": 5, "matricule": "STU-005", "name": "Thomas Dubois",   "email": "t.dubois@edu.crm",        "phone": "778899001", "gender": Gender.M, "photo_url": ""},
    {"id": 6, "matricule": "STU-006", "name": "Awa Diallo",      "email": "awa.diallo@edu.crm",      "phone": "701234567", "gender": Gender.F, "photo_url": ""},
    {"id": 7, "matricule": "STU-007", "name": "Omar Sy",         "email": "omar.sy@edu.crm",         "phone": "782345678", "gender": Gender.M, "photo_url": ""},
    {"id": 8, "matricule": "STU-008", "name": "Fatou Ndiaye",    "email": "fatou.ndiaye@edu.crm",    "phone": "701234568", "gender": Gender.F, "photo_url": ""},
    {"id": 9, "matricule": "STU-009", "name": "Pierre Martin",   "email": "p.martin@edu.crm",        "phone": "771234568", "gender": Gender.M, "photo_url": ""},
    {"id":10, "matricule": "STU-010", "name": "Claire Dubois",   "email": "c.dubois@edu.crm",        "phone": "789876544", "gender": Gender.F, "photo_url": ""},
    {"id":11, "matricule": "STU-011", "name": "Moussa Koné",     "email": "m.kone@edu.crm",          "phone": "764512891", "gender": Gender.M, "photo_url": ""},
    {"id":12, "matricule": "STU-012", "name": "Aïda Mbaye",      "email": "a.mbaye@edu.crm",         "phone": "703322111", "gender": Gender.F, "photo_url": ""},
]

# Nombre de cours par étudiant (simulé)
STUDENT_COURSES = {1: 3, 2: 5, 3: 2, 4: 4, 5: 1, 6: 3, 7: 2, 8: 4, 9: 1, 10: 3, 11: 5, 12: 2}


# ── Routes ────────────────────────────────────────────────────────────────────

@students_bp.route("/")
def list():
    from flask import current_app

    # Paramètres GET
    q        = request.args.get("q", "").strip().lower()
    gender   = request.args.get("gender", "")
    per_page = int(request.args.get("per_page", current_app.config["PAGINATION_DEFAULT"]))
    page     = int(request.args.get("page", 1))

    # --- Filtrage statique (à remplacer par student_service.filter()) ---
    # TODO: Appeler le service pour récupérer la liste des étudiants filtrées 
    filtered = STUDENTS

    if q:
        filtered = [
            s for s in filtered
            if q in s["name"].lower()
            or q in s["email"].lower()
            or q in s["matricule"].lower()
        ]

    if gender:
        filtered = [s for s in filtered if s["gender"].value == gender]
    # --- fin filtrage statique ---

    # Pagination
    total       = len(filtered)
    total_pages = max(1, -(-total // per_page))  # ceil division
    page        = max(1, min(page, total_pages))
    start       = (page - 1) * per_page
    items       = filtered[start:start + per_page]

    # Ajout du nombre de cours à chaque item
    for s in items:
        s["course_count"] = STUDENT_COURSES.get(s["id"], 0)

    return render_template(
        "students/list.html",
        students    = items,
        total       = total,
        page        = page,
        per_page    = per_page,
        total_pages = total_pages,
        q           = q,
        gender      = gender,
        admin= {"name": "Jean Dupont", "photo_url": ""},
    )


@students_bp.route("/create", methods=["GET", "POST"])
def create():
    from app.students.form import StudentForm
    from flask import current_app, flash, redirect
    form = StudentForm()
    if form.validate_on_submit():
        # TODO: student_service.add_student()  avec Alchemy
        flash("Étudiant inscrit avec succès.", "success")
        return redirect(url_for("students.list"))
    return render_template(
        "students/create.html",
        form         = form,
        admin = {"name": "Jean Dupont", "photo_url": ""},
        PHONE_PREFIX = current_app.config["PHONE_PREFIX"],
    )


@students_bp.route("/<string:mat>")
def detail(mat):
    # TODO: student_service.get_student_by_mat(mat) avec Alchemy
    return render_template("students/detail.html")


@students_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    # TODO: student_service.update_student(id)  avec Alchemy
    return render_template("students/edit.html")


@students_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    # TODO: student_service.delete_student(id)  avec Alchemy
    pass