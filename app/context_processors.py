from flask import current_app
from datetime import datetime
from app.models.gender     import Gender
from app.models.speciality import Speciality
from app.enum_ui           import registry
from app.auth.session     import get_session_user


def inject_globals():
    return {
        "APP_NAME":           current_app.config["APP_NAME"],
        "APP_LOGO":           current_app.config["APP_LOGO"],
        "APP_LOGO_WHITE":     current_app.config["APP_LOGO_WHITE"],
        "current_year":       datetime.now().year,
        "PAGINATION_SIZES":   current_app.config["PAGINATION_SIZES"],
        "PAGINATION_DEFAULT": current_app.config["PAGINATION_DEFAULT"],
        "PHONE_PREFIX":       current_app.config["PHONE_PREFIX"],

        # NEW: profil show-more
        "PROFILE_LIST_INITIAL": current_app.config.get("PROFILE_LIST_INITIAL", 5),
        "PROFILE_LIST_STEPS":   current_app.config.get("PROFILE_LIST_STEPS", [10, 20, -1]),

        "Gender":             Gender,
        "Speciality":         Speciality,
        "ev":                 registry.get,
        "session_user":       get_session_user(),
    }