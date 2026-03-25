from flask import Blueprint, render_template, request, url_for, redirect, flash, current_app
from app.models.gender     import Gender
from app.models.speciality import Speciality
from app.services.teacher_service import teacher_service
from app.utils.db_errors import handle_integrity_error
from app.utils.show_more import paginate_show_more
from sqlalchemy.exc import IntegrityError

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")


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
    if not teacher:
        flash("Enseignant introuvable.", "danger")
        return redirect(url_for("teachers.list"))

    # Cours triés du plus récent au plus ancien
    all_courses = sorted(teacher.courses, key=lambda c: c.created_at, reverse=True)

    # Pagination progressive (show more)
    result = paginate_show_more(
        items   = all_courses,
        more    = request.args.get("more", 0, type=int),
        initial = current_app.config.get("PROFILE_LIST_INITIAL", 5),
        steps   = current_app.config.get("PROFILE_LIST_STEPS", [10, 20, -1]),
    )

    return render_template(
        "teachers/detail.html",
        teacher       = teacher,
        courses       = result["items"],
        total_courses = result["total"],
        has_more      = result["has_more"],
        next_more     = result["next_more"],
    )


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