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
        from .models import User, Student, Teacher, Course  # noqa

    # ── Enregistrement des mappings enum_ui ───────────────────────────────────
    from .enum_ui import gender     # noqa
    from .enum_ui import speciality # noqa

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
        from .filters import format_phone
        return format_phone(number)

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

    return app