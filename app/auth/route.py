from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user
from app.models import User
from .forms import LoginForm
from app.auth.session import login_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # utiliser le service ici
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Connexion réussie ! Bienvenue.", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Email ou mot de passe incorrect.", "error")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
def logout():
    # Implementer
    return None