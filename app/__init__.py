from flask import Flask
from config import config
from .extensions import db, migrate
from .context_processors import inject_globals


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # ── Extensions ────────────────────────────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)

    # ── Import des modèles (nécessaire pour Flask-Migrate) ────────────────────
    with app.app_context():
        from .models import User, Student, Teacher, Course

    # ── Enregistrement des mappings enum_ui ───────────────────────────────────
    from .enum_ui import gender
    from .enum_ui import speciality

    # ── Filtres Jinja2 ────────────────────────────────────────────────────────
    app.jinja_env.filters['ord'] = ord

    @app.template_filter('replace_arg')
    def replace_arg(args, key, value):
        d = dict(args)
        d[key] = value
        return '&'.join(f"{k}={v}" for k, v in d.items())

    @app.template_filter('min')
    def min_filter(values):
        return min(values)

    @app.template_filter('format_phone')
    def format_phone_filter(number):
        prefix = app.config.get('PHONE_PREFIX', '+221')
        n = str(number).strip()
        if len(n) == 9:
            return f"{prefix} {n[0:2]} {n[2:5]} {n[5:7]} {n[7:9]}"
        return f"{prefix} {n}"

    @app.template_filter('format_date')
    def format_date_filter(value):
        """
        Formate un objet date ou datetime en chaîne lisible française.
        Exemple : datetime(2023, 9, 15) → "15 Sept 2023"
        Utilisé dans les templates via : {{ course.created_at | format_date }}
        """
        if value is None:
            return ''
        _months = [
            'Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin',
            'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc',
        ]
        return f"{value.day} {_months[value.month - 1]} {value.year}"

    # ── Context processors ────────────────────────────────────────────────────
    app.context_processor(inject_globals)

    # ── Blueprints ────────────────────────────────────────────────────────────
    from .auth.route      import auth_bp
    from .dashboard.route import dashboard_bp
    from .students.route  import students_bp
    from .teachers.route  import teachers_bp
    from .courses.route   import courses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(courses_bp)

    from .cli import register_cli
    register_cli(app)

    return app