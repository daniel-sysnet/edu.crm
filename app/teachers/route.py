from flask import Blueprint, render_template, request
from app.models.gender     import Gender
from app.models.speciality import Speciality

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")


# ── Données statiques de test ─────────────────────────────────────────────────

TEACHERS = [
    {"id": 1, "matricule": "ENS-001", "name": "Marc Tremblay",    "email": "marc.tremblay@edu.crm",   "phone": "771234567", "gender": Gender.M, "speciality": Speciality.DATA,    "photo_url": ""},
    {"id": 2, "matricule": "ENS-002", "name": "Sylvie Laurent",   "email": "sylvie.laurent@edu.crm",  "phone": "769876543", "gender": Gender.F, "speciality": Speciality.WEB,     "photo_url": ""},
    {"id": 3, "matricule": "ENS-003", "name": "Alain Martin",     "email": "alain.martin@edu.crm",    "phone": "704512890", "gender": Gender.M, "speciality": Speciality.NETWORK, "photo_url": ""},
    {"id": 4, "matricule": "ENS-004", "name": "Isabelle Richard", "email": "isabelle.r@edu.crm",      "phone": "783322110", "gender": Gender.F, "speciality": Speciality.AI,      "photo_url": ""},
    {"id": 5, "matricule": "ENS-005", "name": "Robert Dupont",    "email": "robert.d@edu.crm",        "phone": "778899001", "gender": Gender.M, "speciality": Speciality.WEB,     "photo_url": ""},
    {"id": 6, "matricule": "ENS-006", "name": "Claire Petit",     "email": "claire.p@edu.crm",        "phone": "701234567", "gender": Gender.F, "speciality": Speciality.DATA,    "photo_url": ""},
    {"id": 7, "matricule": "ENS-007", "name": "Thomas Moreau",    "email": "t.moreau@edu.crm",        "phone": "771234568", "gender": Gender.M, "speciality": Speciality.AI,      "photo_url": ""},
    {"id": 8, "matricule": "ENS-008", "name": "Nadia Boulanger",  "email": "n.boulanger@edu.crm",     "phone": "789876544", "gender": Gender.F, "speciality": Speciality.NETWORK, "photo_url": ""},
    {"id": 9, "matricule": "ENS-009", "name": "Paul Leclerc",     "email": "p.leclerc@edu.crm",       "phone": "764512891", "gender": Gender.M, "speciality": Speciality.WEB,     "photo_url": ""},
]

TEACHER_COURSES = {1: 2, 2: 4, 3: 3, 4: 2, 5: 1, 6: 3, 7: 2, 8: 1, 9: 4}


# ── Routes ────────────────────────────────────────────────────────────────────

@teachers_bp.route("/")
def list():
    from flask import current_app

    q          = request.args.get("q", "").strip().lower()
    gender     = request.args.get("gender", "")
    speciality = request.args.get("speciality", "")
    per_page   = int(request.args.get("per_page", current_app.config["PAGINATION_DEFAULT"]))
    page       = int(request.args.get("page", 1))

    # --- Filtrage statique ---
    # TODO: Appeler le service pour récupérer la liste des étudiants filtrées 
    filtered = TEACHERS

    if q:
        filtered = [
            t for t in filtered
            if q in t["name"].lower()
            or q in t["email"].lower()
            or q in t["matricule"].lower()
        ]
    if gender:
        filtered = [t for t in filtered if t["gender"].value == gender]

    if speciality:
        filtered = [t for t in filtered if t["speciality"].value == speciality]
    # --- fin filtrage statique ---

    total       = len(filtered)
    total_pages = max(1, -(-total // per_page))
    page        = max(1, min(page, total_pages))
    start       = (page - 1) * per_page
    items       = filtered[start:start + per_page]

    for t in items:
        t["course_count"] = TEACHER_COURSES.get(t["id"], 0)

    return render_template(
        "teachers/list.html",
        teachers    = items,
        total       = total,
        page        = page,
        per_page    = per_page,
        total_pages = total_pages,
        q           = q,
        gender      = gender,
        speciality  = speciality,
    )


@teachers_bp.route("/create", methods=["GET", "POST"])
def create():
    from app.teachers.form import TeacherForm
    from flask import current_app, flash, redirect
    form = TeacherForm()
    if form.validate_on_submit():
        # TODO: teacher_service.add_teacher() avec Alchemy
        flash("Enseignant ajouté avec succès.", "success")
        return redirect(url_for("teachers.list"))
    return render_template(
        "teachers/create.html",
        form         = form,
        admin = {"name": "Jean Dupont", "photo_url": ""},
        PHONE_PREFIX = current_app.config["PHONE_PREFIX"],
    )


@teachers_bp.route("/<str:mat>")
def detail(mat):
    return render_template("teachers/detail.html")


@teachers_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    return render_template("teachers/edit.html")


@teachers_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    pass