from flask import Blueprint, render_template
from app.auth.decorators import login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/")


# ── Données statiques de test ───────────────────────────────────────────────── (supprimer après implémentation service Alchemy)

CURRENT_USER = {
    "name":      "Jean Dupont",
    "photo_url": "",            # Laisser vide pour tester les initiales
}

STATS = {
    "total_students":    1240,
    "total_teachers":    85,
    "total_courses":     42,
    "courses_empty":     8,
    "most_popular_course": "Physique Quantique",
    "total_enrolled":    1156,
    "students_no_course": 84,
    "active_teachers":   72,
}

ACTIVITIES = [
    {
        "date":        "12 Oct 2023",
        "action":      "ajouter",
        "entity_id":   "ETU-001",
        "entity_type": "Étudiant",
        "details":     "Lucas Bernard",
        "user_id":     "ADM-01",
        "user_name":   "Jean Dupont",
    },
    {
        "date":        "12 Oct 2023",
        "action":      "supprimer",
        "entity_id":   "CRS-102",
        "entity_type": "Cours",
        "details":     "Physique Quantique II",
        "user_id":     "ADM-02",
        "user_name":   "Marie Laurent",
    },
    {
        "date":        "11 Oct 2023",
        "action":      "modifier",
        "entity_id":   "ETU-002",
        "entity_type": "Étudiant",
        "details":     "Awa Diallo",
        "user_id":     "ADM-01",
        "user_name":   "Jean Dupont",
    },
    {
        "date":        "10 Oct 2023",
        "action":      "ajouter",
        "entity_id":   "ENS-015",
        "entity_type": "Enseignant",
        "details":     "Dr. Moussa Koné",
        "user_id":     "ADM-01",
        "user_name":   "Jean Dupont",
    },
    {
        "date":        "09 Oct 2023",
        "action":      "ajouter",
        "entity_id":   "CRS-103",
        "entity_type": "Cours",
        "details":     "Algorithmique Avancée",
        "user_id":     "ADM-02",
        "user_name":   "Marie Laurent",
    },
]


# ── Routes ────────────────────────────────────────────────────────────────────

@dashboard_bp.route("/")
@login_required
def index():
    return render_template(
        "dashboard/index.html",
        current_user = CURRENT_USER,
        stats        = STATS,
        activities   = ACTIVITIES,
    )