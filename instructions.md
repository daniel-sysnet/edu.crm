# 📋 Instructions de Collaboration — Edu.CRM

> Ce document est destiné à **tous les membres de l'équipe**. Lisez-le **en entier** avant de toucher au code.

---

## 1. Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.10+** → [python.org](https://www.python.org/downloads/)
- **Git** → [git-scm.com](https://git-scm.com/)
- **Un éditeur** : VS Code recommandé
- **Un compte GitHub** avec accès au dépôt du projet

---

## 2. Récupérer le projet en local

```bash
# 1. Cloner le dépôt (une seule fois)
git clone https://github.com/<ORGANISATION>/edu-crm.git

# 2. Entrer dans le dossier
cd edu-crm

# 3. Créer votre environnement virtuel
python -m venv venv

# 4. Activer l'environnement
# Linux / Mac :
source venv/bin/activate
# Windows :
venv\Scripts\activate

# 5. Installer les dépendances
pip install -r requirements.txt
```

> ⚠️ **Ne commitez JAMAIS le dossier `venv/`.** Il est déjà dans le `.gitignore`.

---

## 3. Lancer l'application

```bash
# Depuis la racine du projet, avec l'environnement activé :
python app/run.py
```

L'application sera accessible sur `http://127.0.0.1:5000`.

---

## 4. Workflow Git — Comment travailler

### 4.1. Règle absolue

> **On ne travaille JAMAIS directement sur `main`.**  
> Chaque fonctionnalité = une branche dédiée.

### 4.2. Avant de commencer à travailler (chaque jour)

```bash
# 1. Se placer sur main
git checkout main

# 2. Récupérer les dernières modifications
git pull origin main

# 3. Retourner sur votre branche
git checkout <votre-branche>

# 4. Intégrer les nouveautés de main dans votre branche
git merge main
```

Si un conflit apparaît, résolvez-le dans votre éditeur, puis :
```bash
git add <fichier_en_conflit>
git commit -m "fix: résolution conflit avec main"
```

### 4.3. Nommage des branches

Le format est strict :

```
<type>/<module>-<description-courte>
```

Exemples :
| Branche | Qui |
|---|---|
| `feature/auth-login-logout` | Étudiant 1 |
| `feature/students-crud` | Étudiant 2 |
| `feature/teachers-crud` | Étudiant 3 |
| `feature/courses-crud` | Étudiant 4 |
| `feature/dashboard-ui` | Étudiant 5 |
| `fix/auth-session-bug` | Étudiant 1 |
| `setup/project-structure` | Admin |

### 4.4. Faire un commit

```bash
git add .
git commit -m "<type>: <description>"
```

**Types de commit autorisés :**

| Type | Usage |
|---|---|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `style` | Modification CSS / template (pas de logique) |
| `refactor` | Restructuration sans changement de comportement |
| `docs` | Documentation |
| `setup` | Configuration / structure projet |

**Exemples :**
```
feat: ajout formulaire de connexion
feat: implémentation list_students dans le service
fix: correction redirect après logout
style: mise en forme du tableau étudiants
docs: mise à jour du README
```

### 4.5. Pousser votre branche et créer une Pull Request

```bash
# Pousser votre branche sur GitHub
git push origin <votre-branche>
```

Ensuite sur GitHub :
1. Allez sur le dépôt
2. Cliquez sur **"Compare & Pull Request"**
3. **Base** : `main` ← **Compare** : `<votre-branche>`
4. Donnez un titre clair et une description de ce que vous avez fait
5. Assignez **l'Admin** comme reviewer
6. **Ne fusionnez pas vous-même.** C'est l'Admin qui valide et merge.

---

## 5. Ce que vous n'avez PAS le droit de faire

| Interdit | Raison |
|---|---|
| Commiter sur `main` directement | Risque de casser le projet pour tout le monde |
| Merger votre propre PR | L'Admin vérifie et valide |
| Modifier les fichiers d'un autre module sans accord | Chacun est responsable de son module |
| Commiter `venv/`, `__pycache__/`, `.env` | Fichiers locaux uniquement |
| Changer `app/config.py`, `app/run.py`, `app/__init__.py` sans accord Admin | Fichiers partagés critiques |
| Renommer des fonctions de service existantes | Casse le code des autres |

---

## 6. Ajouter une dépendance Python

Si vous avez besoin d'un nouveau package :

```bash
# 1. Installer le package
pip install <nom-du-package>

# 2. Mettre à jour requirements.txt
pip freeze > requirements.txt

# 3. Commiter
git add requirements.txt
git commit -m "setup: ajout dépendance <nom-du-package>"
```

> Les autres devront faire `pip install -r requirements.txt` après un `git pull`.

---

## 7. Structure des fichiers — Où travailler

```
edu-crm/
├── app/
│   ├── __init__.py              ← Admin uniquement
│   ├── config.py                ← Admin uniquement
│   ├── run.py                   ← Admin uniquement
│   ├── auth/
│   │   ├── __init__.py
│   │   └── route.py             ← Étudiant 1
│   ├── students/
│   │   ├── __init__.py
│   │   └── route.py             ← Étudiant 2
│   ├── teachers/
│   │   ├── __init__.py
│   │   └── route.py             ← Étudiant 3
│   ├── courses/
│   │   ├── __init__.py
│   │   └── route.py             ← Étudiant 4
│   ├── dashboard/
│   │   ├── __init__.py
│   │   └── route.py             ← Étudiant 5
│   ├── services/
│   │   ├── __init__.py
│   │   ├── student_service.py   ← Étudiant 2
│   │   ├── teacher_service.py   ← Étudiant 3
│   │   └── course_service.py    ← Étudiant 4
│   └── templates/
│       ├── base.html            ← Étudiant 5 (Admin valide)
│       ├── auth/
│       │   └── login.html       ← Étudiant 1
│       ├── students/
│       │   ├── list.html        ← Étudiant 2
│       │   └── create.html      ← Étudiant 2
│       ├── teachers/
│       │   ├── list.html        ← Étudiant 3
│       │   └── create.html      ← Étudiant 3
│       ├── courses/
│       │   ├── list.html        ← Étudiant 4
│       │   └── create.html      ← Étudiant 4
│       └── dashboard/
│           └── index.html       ← Étudiant 5
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 8. Communication

- **Avant de commencer** votre partie : prévenez dans le groupe.
- **En cas de blocage** : demandez de l'aide, ne restez pas bloqué seul.
- **Avant de modifier un fichier partagé** : demandez à l'Admin.
- **Quand votre PR est prête** : signalez-le dans le groupe.

---

## 9. Résumé en 5 règles

1. **Toujours pull `main` avant de travailler**
2. **Une branche par fonctionnalité**
3. **Des commits clairs et fréquents**
4. **Pull Request → Review Admin → Merge**
5. **Ne touchez qu'à vos fichiers**