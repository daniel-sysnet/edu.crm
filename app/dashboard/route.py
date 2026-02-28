from flask import Blueprint, render_template
from app.auth.route import login_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='')


@dashboard_bp.route('/')
@login_required
def index():
    # Les stats seront alimentées par les services des autres étudiants
    # Pour l'instant on passe des valeurs à 0 — à mettre à jour en phase finale
    stats = {
        'nb_students': 0,   # remplacer par len(list_students())
        'nb_teachers': 0,   # remplacer par len(list_teachers())
        'nb_courses':  0,   # remplacer par len(list_courses())
    }
    return render_template('dashboard/index.html', stats=stats)