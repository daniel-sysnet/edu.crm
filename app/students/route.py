from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.students.student_service import student_service
from app.models.gender import Genre

students_bp = Blueprint("students", __name__, url_prefix="/students")


@students_bp.route("/")
def list():
    q        = request.args.get("q", "").strip()
    gender   = request.args.get("gender", "")
    per_page = int(request.args.get("per_page", current_app.config["PAGINATION_DEFAULT"]))
    page     = int(request.args.get("page", 1))

    genre_enum = None
    if gender == "M":
        genre_enum = Genre.M
    elif gender == "F":
        genre_enum = Genre.F

    filtered = student_service.listStudents(q, genre_enum)

    total       = len(filtered)
    total_pages = max(1, -(-total // per_page))
    page        = max(1, min(page, total_pages))
    start       = (page - 1) * per_page
    items       = filtered[start:start + per_page]

    return render_template(
        "students/list.html",
        students=items,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        q=q,
        gender=gender,
        admin={"name": "Jean Dupont", "photo_url": ""}
    )


@students_bp.route("/create", methods=["GET", "POST"])
def create():
    from app.students.form import StudentForm

    form = StudentForm()

    if form.validate_on_submit():
        genre_enum = Genre.M if form.genre.data == "M" else Genre.F

        student_service.addStudent(
            name=form.name.data,
            email=form.email.data,
            genre=genre_enum,
            birthday=form.birthday.data,
            adresse=form.adresse.data,
            telephone=form.telephone.data
        )

        flash("Étudiant inscrit avec succès.", "success")
        return redirect(url_for("students.list"))

    return render_template(
        "students/create.html",
        form=form,
        admin={"name": "Jean Dupont", "photo_url": ""},
        PHONE_PREFIX=current_app.config["PHONE_PREFIX"]
    )


@students_bp.route("/<string:matricule>")
def detail(matricule):
    student = student_service.getByMatricule(matricule)

    if not student:
        flash("Étudiant introuvable", "danger")
        return redirect(url_for("students.list"))

    return render_template(
        "students/detail.html",
        student=student
    )


@students_bp.route("/<string:matricule>/edit", methods=["GET", "POST"])
def edit(matricule):
    from app.students.form import StudentForm

    student = student_service.getByMatricule(matricule)

    if not student:
        flash("Étudiant introuvable", "danger")
        return redirect(url_for("students.list"))

    form = StudentForm(obj=student)

    if form.validate_on_submit():
        genre_enum = Genre.M if form.genre.data == "M" else Genre.F

        student_service.updateStudent(
            matricule=matricule,
            name=form.name.data,
            email=form.email.data,
            genre=genre_enum,
            birthday=form.birthday.data,
            adresse=form.adresse.data,
            telephone=form.telephone.data
        )

        flash("Étudiant modifié avec succès", "success")
        return redirect(url_for("students.list"))

    return render_template(
        "students/edit.html",
        form=form,
        student=student
    )


@students_bp.route("/<string:matricule>/delete", methods=["POST"])
def delete(matricule):
    student = student_service.deleteStudent(matricule)

    if not student:
        flash("Étudiant introuvable", "danger")
    else:
        flash("Étudiant supprimé avec succès", "success")

    return redirect(url_for("students.list"))