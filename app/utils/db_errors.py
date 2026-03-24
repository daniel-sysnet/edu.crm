from sqlalchemy.exc import IntegrityError

UNIQUE_FIELD_MAP = {
    "email": ("email", "Cette adresse email est déjà utilisée."),
    "phone": ("phone", "Ce numéro de téléphone est déjà utilisé."),
}

def handle_integrity_error(e: IntegrityError, form):
    """Attache l'erreur SQL au champ WTForms correspondant."""
    error_str = str(e.orig).lower()
    for keyword, (field_name, message) in UNIQUE_FIELD_MAP.items():
        if keyword in error_str and hasattr(form, field_name):
            getattr(form, field_name).errors.append(message)
            return
    form.errors.setdefault("__general__", []).append("Erreur de doublon inattendue.")