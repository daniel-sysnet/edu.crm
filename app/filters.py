from flask import current_app


def format_phone(number: str) -> str:
    """
    Formate un numéro sénégalais.
    Entrée  : "757447874" (9 chiffres)
    Sortie  : "+221 75 744 78 74"
    """
    prefix = current_app.config.get('PHONE_PREFIX', '+221')
    n = str(number).strip()
    if len(n) == 9:
        return f"{prefix} {n[0:2]} {n[2:5]} {n[5:7]} {n[7:9]}"
    return f"{prefix} {n}"