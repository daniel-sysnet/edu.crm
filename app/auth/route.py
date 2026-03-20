from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.auth_service import AuthService
from app.auth.decorators import login_required


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_service = AuthService()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        login    = request.form.get('login', '').strip()
        password = request.form.get('password', '').strip()

        user = auth_service.login(login, password)

        if user:
            session['user_id'] = user.id
            session['login']   = user.login
            session['name']    = user.name
            flash(f"Bienvenue {user.name} ! Connexion réussie.", "success")
            return redirect(url_for('dashboard.index'))
        else:
            flash("Identifiant ou mot de passe incorrect.", "danger")

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    name = session.get('name', 'Utilisateur')
    session.clear()
    flash(f"Au revoir {name}, vous êtes déconnecté.", "info")
    return redirect(url_for('auth.login'))