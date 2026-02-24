# Edu.CRM

Mini système de gestion interne pour une école, développé avec **Flask** et **Blueprints**.

## Fonctionnalités

- Authentification (login / logout)
- Gestion des étudiants (liste, ajout, suppression)
- Gestion des enseignants (liste, ajout, suppression)
- Gestion des cours (liste, création, assignation)
- Dashboard statistique

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/daniel-sysnet/edu.crm
cd edu-crm

# Ouvrir le projet avec vs code
code .

# Afficher le terminal de vscode
# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Lancer l'application

```bash
python app/run.py
```

Accéder à : `http://127.0.0.1:5000`

## Structure du projet

```
edu-crm/
├── app/
│   ├── __init__.py          # Application Factory
│   ├── config.py            # Configuration
│   ├── run.py               # Point d'entrée
│   ├── auth/                # Blueprint authentification
│   ├── students/            # Blueprint étudiants
│   ├── teachers/            # Blueprint enseignants
│   ├── courses/             # Blueprint cours
│   ├── dashboard/           # Blueprint dashboard
│   ├── services/            # Logique métier
│   └── templates/           # Templates HTML
├── .gitignore
├── requirements.txt
└── README.md
```

## Équipe

| Membre | Module |
|---|---|
| Admin | Structure, intégration, validation |
| Étudiant 1 | Auth & Sécurité |
| Étudiant 2 | Students |
| Étudiant 3 | Teachers |
| Étudiant 4 | Courses |
| Étudiant 5 | Dashboard & UI |

## Règles de collaboration

- Ne jamais travailler directement sur `main`
- Une branche par fonctionnalité (`feature/module-description`)
- Pull Request obligatoire avant merge
- Commits clairs : `feat:`, `fix:`, `style:`, `docs:`

> Consulter `instructions.md` pour le guide complet.