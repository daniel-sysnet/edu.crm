from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from app.services.auth_service import AuthService


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        login    = request.form.get('login', '').strip()
        password = request.form.get('password', '').strip()

        auth_service = AuthService()
        user = auth_service.login(login, password)

        if user:
            session['user_id'] = user.id
            session['login']   = user.login
            flash(f"Bienvenue {user.login} ! Connexion réussie.", "success")
            return redirect(url_for('dashboard.index'))
        else:
            flash("Identifiant ou mot de passe incorrect.", "danger")

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    login = session.get('login', 'Utilisateur')
    session.clear()
    flash(f"Au revoir {login}, vous êtes déconnecté.", "info")
    return redirect(url_for('auth.login'))