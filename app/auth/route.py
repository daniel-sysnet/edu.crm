from flask import Blueprint, render_template, flash, redirect, url_for
from app.auth.forms import LoginForm
from app.auth.session import login_user, get_session_user
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

auth_service = AuthService()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = auth_service.login(form.email.data, form.password.data)
        if user:
            login_user(user)
            flash(f"Bienvenue {user.username} ! Connexion réussie.", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Email ou mot de passe incorrect.", "error")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
def logout():
    from flask import session
    username = get_session_user()
    session.clear()
    flash(f"Au revoir, vous êtes déconnecté.", "info")
    return redirect(url_for("auth.login"))