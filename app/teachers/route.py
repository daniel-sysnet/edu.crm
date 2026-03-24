from flask import Blueprint, render_template, request, url_for, redirect
from app.models.gender     import Gender
from app.models.speciality import Speciality
from app.services.teacher_service import TeacherService
from app.utils.db_errors import handle_integrity_error
from sqlalchemy.exc import IntegrityError

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")
teacher_service = TeacherService()


@teachers_bp.route("/")
def list():
    from flask import current_app

    q          = request.args.get("q", "").strip().lower()
    gender     = request.args.get("gender", "")
    speciality = request.args.get("speciality", "")
    per_page   = int(request.args.get("per_page", current_app.config["PAGINATION_DEFAULT"]))
    page       = int(request.args.get("page", 1))

    filtered = teacher_service.listTeachers(query=q, gender=Gender(gender) if gender else None, speciality=Speciality(speciality) if speciality else None)
    
    total       = len(filtered)
    total_pages = max(1, -(-total // per_page))
    page        = max(1, min(page, total_pages))
    start       = (page - 1) * per_page
    items       = filtered[start:start + per_page]

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
        try:
            teacher_service.addTeacher(
                name=form.name.data or "",
                email=form.email.data or "",
                speciality=Speciality(form.speciality.data),
                gender=Gender(form.gender.data),
                dob=form.dob.data,
                address=form.address.data or "",
                phone=form.phone.data or "",
            )
            flash("Enseignant ajouté avec succès.", "success")
            return redirect(url_for("teachers.list"))
        except IntegrityError as e:
            handle_integrity_error(e, form)
    return render_template(
        "teachers/create.html",
        form         = form,
        PHONE_PREFIX = current_app.config["PHONE_PREFIX"],
    )


@teachers_bp.route("/<string:mat>")
def detail(mat):
    teacher = teacher_service.getByMatricule(mat)
    return render_template("teachers/detail.html", matricule=mat)


@teachers_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    return render_template("teachers/edit.html")


@teachers_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    from flask import flash
    if teacher_service.deleteTeacher(id):
        flash("Enseignant supprimé avec succès.", "success")
    else:
        flash("Enseignant introuvable.", "danger")
    return redirect(url_for("teachers.list"))