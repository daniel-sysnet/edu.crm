from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.teacher_service import TeacherService
from app.models.gender import Gender
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
    q = request.args.get("q", "").strip() or None
    gender_str = request.args.get("gender", "").strip() or None
    speciality_str = request.args.get("speciality", "").strip() or None
    per_page = request.args.get("per_page", type=int, default=None)
    page = request.args.get("page", type=int, default=None)

    gender_filter: Optional[Gender] = Gender(gender_str) if gender_str else None
    speciality_filter: Optional[Speciality] = Speciality(speciality_str) if speciality_str else None

    teachers = teacher_service.listTeachers(
        query=q,
        gender=gender_filter,
        speciality=speciality_filter,
        per_page=per_page,
        page=page,
    )
    return render_template(
        "teachers/list.html",
        teachers=teachers,
        genders=Gender,
        specialities=Speciality
    )


# GET & POST /teachers/create
@teachers_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name       = request.form.get("name", "").strip()
        email      = request.form.get("email", "").strip()
        speciality = request.form.get("speciality", "").strip()
        gender     = request.form.get("gender", "").strip()
        birthday   = request.form.get("birthday", "").strip()
        address    = request.form.get("address", "").strip()
        phone      = request.form.get("phone", "").strip()

        if not all([name, email, speciality, gender, birthday, address, phone]):
            flash("Tous les champs sont obligatoires.", "danger")
            return render_template(
                "teachers/create.html",
                genders=Gender, specialities=Speciality
            )
        try:
            teacher = teacher_service.addTeacher(
                name=name,
                email=email,
                speciality=Speciality(speciality),
                gender=Gender(gender),
                birthday=date.fromisoformat(birthday),
                address=address,
                phone=phone
            )
            flash(f"Enseignant '{teacher.name}' ajouté avec succès.", "success")
            return redirect(url_for("teachers.detail", id=teacher.id))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template(
                "teachers/create.html",
                genders=Gender, specialities=Speciality
            )

    return render_template(
        "teachers/create.html",
        genders=Gender, specialities=Speciality
    )


# GET /teachers/<id>
@teachers_bp.route("/<int:id>")
def detail(id: int):
    teacher = teacher_service.getById(id)
    if teacher is None:
        flash("Enseignant introuvable.", "warning")
        return redirect(url_for("teachers.list"))
    return render_template("teachers/detail.html", teacher=teacher)


@teachers_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    return render_template("teachers/edit.html")


@teachers_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    pass