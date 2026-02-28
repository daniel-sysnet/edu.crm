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
python -m venv .venv
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