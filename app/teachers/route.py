from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.teacher_service import TeacherService
from app.models.gender import Gender
from app.models.speciality import Speciality
from typing import Optional
from datetime import date

teachers_bp = Blueprint(
    "teachers",
    __name__,
    template_folder="../../templates/teachers",
    url_prefix="/teachers",
)

teacher_service = TeacherService()


# GET /teachers
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
        name      = request.form.get("name", "").strip()
        email     = request.form.get("email", "").strip()
        speciality = request.form.get("speciality", "").strip()
        gender     = request.form.get("gender", "").strip()
        birthday  = request.form.get("birthday", "").strip()
        adresse   = request.form.get("adresse", "").strip()
        telephone = request.form.get("telephone", "").strip()

        if not all([name, email, speciality, gender, birthday, adresse, telephone]):
            flash("Tous les champs sont obligatoires.", "danger")
            return render_template(
                "teachers/create.html",
                genders=Gender, specialities=Speciality
            )
        try:
            teacher = teacher_service.addTeacher(
                name=name,
                email=email,
                specialty=Speciality(speciality),
                gender=Gender(gender),
                birthday=date.fromisoformat(birthday),
                adresse=adresse,
                telephone=telephone
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


# POST /teachers/delete/<id>
@teachers_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id: int):
    teacher = teacher_service.deleteTeacher(id)
    if teacher:
        flash(f"Enseignant '{teacher.name}' supprimé avec succès.", "success")
    else:
        flash("Enseignant introuvable.", "warning")
    return redirect(url_for("teachers.list"))