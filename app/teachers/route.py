from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.teacher_service import TeacherService
from app.model.genre import Genre
from app.model.speciality import Speciality
from typing import Optional
from datetime import date

teachers_bp = Blueprint(
    "teachers",
    _name_,
    template_folder="../../templates/teachers",
    url_prefix="/teachers",
)

teacher_service = TeacherService()


# GET /teachers
@teachers_bp.route("/")
def list():
    query         = request.args.get("query", "").strip() or None
    genre_str     = request.args.get("genre", "").strip() or None
    specialty_str = request.args.get("specialty", "").strip() or None

    genre_filter:     Optional[Genre]      = Genre(genre_str)           if genre_str      else None
    specialty_filter: Optional[Speciality] = Speciality(specialty_str)  if specialty_str  else None

    teachers = teacher_service.listTeachers(
        query=query,
        genre=genre_filter,
        specialty=specialty_filter
    )
    return render_template(
        "teachers/list.html",
        teachers=teachers,
        genres=Genre,
        specialities=Speciality
    )


# GET & POST /teachers/create
@teachers_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name      = request.form.get("name", "").strip()
        email     = request.form.get("email", "").strip()
        specialty = request.form.get("specialty", "").strip()
        genre     = request.form.get("genre", "").strip()
        birthday  = request.form.get("birthday", "").strip()
        adresse   = request.form.get("adresse", "").strip()
        telephone = request.form.get("telephone", "").strip()

        if not all([name, email, specialty, genre, birthday, adresse, telephone]):
            flash("Tous les champs sont obligatoires.", "danger")
            return render_template(
                "teachers/create.html",
                genres=Genre, specialities=Speciality
            )
        try:
            teacher = teacher_service.addTeacher(
                name=name,
                email=email,
                specialty=Speciality(specialty),
                genre=Genre(genre),
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
                genres=Genre, specialities=Speciality
            )

    return render_template(
        "teachers/create.html",
        genres=Genre, specialities=Speciality
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