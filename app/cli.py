"""
cli.py – Seed réaliste avec données sénégalaises.

Idempotence :
  - Chaque lancement génère un batch_id unique (4 hex, ex: "a3f9").
  - Les emails sont suffixés → jamais de doublon entre runs.
  - `flask seed` peut être relancé autant de fois que voulu.

Compatibilité modèles :
  - Teacher  : matricule  généré manuellement (format ENS-XXXXXXXX)
  - Student  : matricule  généré manuellement (format STU-XXXXXXXX)
  - Course   : code       généré manuellement (format CRS-XXXXXXXX)
  (les méthodes statiques generate_matricule/generate_code n'existent plus)
"""

import uuid
import secrets
import random
from datetime import date

from flask import Flask

from app.extensions import db
from app.models import User, Student, Teacher, Course
from app.models.gender     import Gender
from app.models.speciality import Speciality


# ── Helpers matricule/code (calqués sur les modèles) ─────────────────────────

def _slug(nom: str) -> str:
    import unicodedata
    normalized = unicodedata.normalize("NFD", nom)
    ascii_nom  = normalized.encode("ascii", "ignore").decode("ascii")
    return ascii_nom.lower().replace(" ", ".")

def _new_matricule_teacher() -> str:
    return f"ENS-{uuid.uuid4().hex[:8].upper()}"

def _new_matricule_student() -> str:
    return f"STU-{uuid.uuid4().hex[:8].upper()}"

def _new_code_course() -> str:
    return f"CRS-{uuid.uuid4().hex[:8].upper()}"


# ── Données sénégalaises ──────────────────────────────────────────────────────

PRENOMS_H = [
    "Mamadou", "Ibrahima", "Cheikh", "Moussa", "Abdou", "Ousmane",
    "Modou", "Lamine", "Serigne", "Pape", "Babacar", "Assane",
    "Saliou", "El Hadji", "Thierno", "Malick", "Idrissa", "Boubacar",
    "Alioune", "Issa", "Aliou", "Seydou", "Daouda", "Mor", "Biram",
]

PRENOMS_F = [
    "Fatou", "Mariama", "Aïssatou", "Ndéye", "Coumba", "Rokhaya",
    "Khady", "Adja", "Aminata", "Sokhna", "Mame", "Binta",
    "Astou", "Dieynaba", "Yacine", "Ramatoulaye", "Seynabou",
    "Nabou", "Oumou", "Penda", "Aby", "Ngoné", "Kiné", "Maty", "Ndaw",
]

NOMS_DE_FAMILLE = [
    "Diallo", "Ndiaye", "Fall", "Sarr", "Diop", "Sow", "Mbaye",
    "Thiam", "Diouf", "Ba", "Camara", "Cissé", "Gueye", "Mboup",
    "Faye", "Touré", "Sy", "Badji", "Manga", "Diatta", "Sène",
    "Ndoye", "Konaté", "Traoré", "Kouyaté", "Diagne", "Lô", "Diaw",
    "Tine", "Dème", "Kane", "Bâ", "Tall", "Coulibaly", "Dabo",
]

VILLES = [
    "Dakar", "Thiès", "Saint-Louis", "Ziguinchor", "Kaolack",
    "Touba", "Mbour", "Diourbel", "Louga", "Fatick",
    "Tambacounda", "Kolda", "Sédhiou", "Kaffrine", "Matam",
]

COURS_CATALOGUE = [
    "Algorithmique & Structures de données",
    "Développement Web – HTML/CSS/JS",
    "Développement Web – React & Next.js",
    "Développement Web – Django/Flask",
    "Bases de données relationnelles (SQL)",
    "Bases de données NoSQL",
    "Réseaux & Protocoles TCP/IP",
    "Sécurité informatique & Cybersécurité",
    "Systèmes d'exploitation Linux",
    "Programmation orientée objet – Python",
    "Programmation orientée objet – Java",
    "Développement mobile – Flutter",
    "Développement mobile – React Native",
    "Intelligence artificielle & Machine Learning",
    "Cloud Computing & DevOps",
    "Génie logiciel & UML",
    "Mathématiques pour l'informatique",
    "Statistiques & Probabilités",
    "Algèbre linéaire",
    "Analyse numérique",
    "Communication professionnelle",
    "Anglais technique",
    "Français professionnel",
    "Gestion de projet agile (Scrum/Kanban)",
    "Management des Systèmes d'Information",
    "Comptabilité générale",
    "Marketing digital",
    "Droit des nouvelles technologies",
    "Entrepreneuriat & Start-up",
    "Éthique professionnelle & RSE",
    "Architecture des ordinateurs",
    "Compilation & Langages formels",
    "Traitement du signal & Image",
    "Internet des Objets (IoT)",
    "Big Data & Hadoop",
    "Blockchain & Web3",
    "Tests logiciels & Qualité",
    "API REST & Microservices",
    "Virtualisation & Conteneurs (Docker/K8s)",
    "Recherche opérationnelle",
]

# Préfixes mobiles sénégalais valides (numéro à 9 chiffres)
PREFIXES_MOBILE = ["70", "75", "76", "77", "78"]


def _phone() -> str:
    return f"{random.choice(PREFIXES_MOBILE)}{random.randint(1_000_000, 9_999_999)}"


def _nom(genre: Gender) -> str:
    pool = PRENOMS_H if genre == Gender.M else PRENOMS_F
    return f"{random.choice(pool)} {random.choice(NOMS_DE_FAMILLE)}"


def _email(nom: str, batch: str, i:int) -> str:
    import unicodedata
    normalized = unicodedata.normalize("NFD", nom)
    ascii_nom  = normalized.encode("ascii", "ignore").decode("ascii")
    slug = ascii_nom.lower().replace(" ", ".")
    return f"{_slug(nom)}.{batch}.{i:03d}@educrm.sn"


# ── Commande CLI ──────────────────────────────────────────────────────────────

def register_cli(app: Flask) -> None:

    @app.cli.command("seed")
    def seed():
        """
        Remplit la base avec des données réalistes sénégalaises.
        Idempotent : peut être relancé sans erreur (batch_id unique à chaque run).
        """

        batch = secrets.token_hex(2)   # ex: "a3f9"
        print(f"\n🌱  Seed batch [{batch}] démarré …\n")

        # ── Admin (créé une seule fois) ───────────────────────────────────────
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", email="admin@educrm.sn")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.flush()
            admin.matricule = User.generate_matricule(admin.id)
            db.session.commit()
            print("  ✅  Admin créé")
        else:
            print("  ⏭️   Admin existe déjà, ignoré")

        # ── Enseignants (20) ──────────────────────────────────────────────────
        teachers = []
        for i in range(20):
            genre = random.choice([Gender.M, Gender.F])
            nom   = _nom(genre)
            t = Teacher(
                matricule  = _new_matricule_teacher(),
                name       = nom,
                email      = _email(nom, batch, i),
                phone      = _phone(),
                gender     = genre,
                speciality = random.choice(list(Speciality)),
                dob        = date(
                    random.randint(1970, 1990),
                    random.randint(1, 12),
                    random.randint(1, 28),
                ),
                address = random.choice(VILLES),
            )
            db.session.add(t)
            teachers.append(t)

        db.session.commit()
        print(f"  ✅  {len(teachers)} enseignants créés")

        # ── Cours (40) ───────────────────────────────────────────────────────
        catalogue = COURS_CATALOGUE.copy()
        random.shuffle(catalogue)

        courses = []
        for titre in catalogue[:40]:
            c = Course(
                code       = _new_code_course(),
                title      = titre,
                teacher_id = random.choice(teachers).id,
            )
            db.session.add(c)
            courses.append(c)

        db.session.commit()
        print(f"  ✅  {len(courses)} cours créés")

        # ── Étudiants (300) ──────────────────────────────────────────────────
        students = []
        for i in range(300):
            genre = random.choice([Gender.M, Gender.F])
            nom   = _nom(genre)
            s = Student(
                matricule = _new_matricule_student(),
                name      = nom,
                email     = _email(nom, batch, i),
                phone     = _phone(),
                gender    = genre,
                dob       = date(
                    random.randint(1998, 2005),
                    random.randint(1, 12),
                    random.randint(1, 28),
                ),
                address = random.choice(VILLES),
            )
            s.courses = random.sample(courses, k=random.randint(2, 5))
            db.session.add(s)
            students.append(s)

        db.session.commit()
        print(f"  ✅  {len(students)} étudiants créés")

        print(f"\n🎉  Seed batch [{batch}] terminé avec succès !\n")