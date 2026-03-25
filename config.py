import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY                     = os.environ.get("SECRET_KEY", "dev-secret-key")
    WTF_CSRF_ENABLED               = False
    APP_NAME                       = "Edu.CRM"
    APP_LOGO                       = "img/logo.png"
    APP_LOGO_WHITE                 = "img/logo-white.png"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pagination
    PAGINATION_SIZES   = [5, 10, 20, 30]
    PAGINATION_DEFAULT = PAGINATION_SIZES[0]

    # Téléphone
    PHONE_PREFIX = "+221"

    # ── Profil : "Afficher plus" (GET) ───────────────────────────────────────
    # Paliers cumulatifs : initial=5, puis +10, +20, tout
    #   more=0 → 5
    #   more=1 → 15  (5+10)
    #   more=2 → 35  (5+10+20)
    #   more=3 → tout
    PROFILE_LIST_INITIAL = 5
    PROFILE_LIST_STEPS   = [10, 20, -1]


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///educrm.db"


class ProductionConfig(Config):
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "").replace(
        "postgres://", "postgresql://"
    )


config = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "default":     DevelopmentConfig,
}