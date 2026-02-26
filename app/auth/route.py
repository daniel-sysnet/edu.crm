from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


USERS = [
    {'id': 1, 'username': 'admin',    'password': 'admin123',    'role': 'admin'},
    {'id': 2, 'username': 'etudiant', 'password': 'etudiant123', 'role': 'etudiant'},
    {'id': 3, 'username': 'prof',     'password': 'prof123',     'role': 'enseignant'},
]


def login_required(f):
    """Redirige vers /auth/login si l'utilisateur n'est pas connecté."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Vous devez être connecté pour accéder à cette page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()


        user = next(
            (u for u in USERS if u['username'] == username and u['password'] == password),
            None
        )

        if user:
            session['user_id']  = user['id']
            session['username'] = user['username']
            session['role']     = user['role']
            flash(f"Bienvenue {user['username']} ! Connexion réussie.", "success")
            return redirect(url_for('dashboard.index'))
        else:
            flash("Identifiant ou mot de passe incorrect.", "danger")

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'Utilisateur')
    session.clear()
    flash(f"Au revoir {username}, vous êtes déconnecté.", "info")
    return redirect(url_for('auth.login'))