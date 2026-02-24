# 🗺️ Plan de Projet — Edu.CRM

> Ce document décrit **l'ordre exact** dans lequel le projet doit avancer.  
> Chaque phase a un **point de revue** où l'Admin vérifie avant de passer à la suite.

---

## Vue d'ensemble des phases

| Phase | Nom | Qui | Durée estimée | Dépend de |
|---|---|---|---|---|
| 0 | Initialisation du projet | Admin | Jour 1 | — |
| 1 | Socle UI + Authentification | Étudiant 5 + Étudiant 1 | Jour 1–2 | Phase 0 |
| 2 | Modules Students & Teachers | Étudiant 2 + Étudiant 3 (en parallèle) | Jour 2–3 | Phase 1 |
| 3 | Module Courses | Étudiant 4 | Jour 3–4 | Phase 2 |
| 4 | Dashboard statistique | Étudiant 5 | Jour 4 | Phase 3 |
| 5 | Intégration finale & tests | Tout le monde | Jour 5 | Phase 4 |

---

## PHASE 0 — Initialisation du projet

**Responsable : Admin**  
**Branche : `main` (commit initial) puis `setup/project-structure`**

### Tâches dans l'ordre

| # | Tâche | Fichier(s) concerné(s) |
|---|---|---|
| 0.1 | Créer le dépôt GitHub | — |
| 0.2 | Ajouter les 5 collaborateurs | Settings → Collaborators |
| 0.3 | Créer le `.gitignore` | `.gitignore` |
| 0.4 | Créer le `requirements.txt` avec Flask | `requirements.txt` |
| 0.5 | Créer `app/run.py` | `app/run.py` |
| 0.6 | Créer `app/__init__.py` avec `create_app()` vide | `app/__init__.py` |
| 0.7 | Créer `app/config.py` | `app/config.py` |
| 0.8 | Créer les dossiers de chaque module avec `__init__.py` vides et `route.py` vides | Tous les modules |
| 0.9 | Créer `app/services/__init__.py` et les 3 fichiers service vides | `app/services/` |
| 0.10 | Créer le dossier `app/templates/` et ses sous-dossiers vides | `app/templates/` |
| 0.11 | Créer le `README.md` | `README.md` |
| 0.12 | Pousser sur `main` | — |

### Structure après Phase 0

```
edu-crm/
├── app/
│   ├── __init__.py              ← create_app() basique
│   ├── config.py                ← SECRET_KEY, DEBUG
│   ├── run.py                   ← point d'entrée
│   ├── auth/
│   │   ├── __init__.py          ← vide
│   │   └── route.py             ← vide (juste un commentaire)
│   ├── students/
│   │   ├── __init__.py
│   │   └── route.py
│   ├── teachers/
│   │   ├── __init__.py
│   │   └── route.py
│   ├── courses/
│   │   ├── __init__.py
│   │   └── route.py
│   ├── dashboard/
│   │   ├── __init__.py
│   │   └── route.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── student_service.py   ← vide
│   │   ├── teacher_service.py   ← vide
│   │   └── course_service.py    ← vide
│   └── templates/
│       ├── auth/
│       ├── students/
│       ├── teachers/
│       ├── courses/
│       └── dashboard/
├── .gitignore
├── requirements.txt             ← Flask uniquement
└── README.md
```

### ✅ Point de revue 0

- [ ] Le dépôt est accessible par tous
- [ ] `python app/run.py` démarre sans erreur (page 404 = normal)
- [ ] La structure des dossiers est complète
- [ ] Chaque collaborateur peut cloner et lancer le projet

---

## PHASE 1 — Socle UI + Authentification

> **Ces deux tâches se font en parallèle** mais Étudiant 5 commence légèrement avant.

---

### Étudiant 5 — base.html & Navbar

**Branche : `feature/dashboard-base-html`**

| # | Tâche | Fichier(s) |
|---|---|---|
| 1.1 | Créer `base.html` avec structure HTML complète | `app/templates/base.html` |
| 1.2 | Ajouter la navbar avec liens vers : /, /students, /teachers, /courses, /login, /logout | `app/templates/base.html` |
| 1.3 | Ajouter la zone d'affichage des flash messages | `app/templates/base.html` |
| 1.4 | Ajouter le bloc `{% block content %}{% endblock %}` | `app/templates/base.html` |
| 1.5 | Créer un `dashboard/index.html` basique qui hérite de base.html (juste un titre "Dashboard") | `app/templates/dashboard/index.html` |
| 1.6 | Créer la route `/` dans `dashboard/route.py` qui affiche `index.html` | `app/dashboard/route.py` |
| 1.7 | Enregistrer le blueprint dashboard dans `create_app()` | **Demander merge Admin** |
| 1.8 | **PR → Admin review → Merge** | — |

---

### Étudiant 1 — Authentification

**Branche : `feature/auth-login-logout`**  
**Commence après que `base.html` soit mergé (ou sur la même base)**

| # | Tâche | Fichier(s) |
|---|---|---|
| 1.9 | Définir les utilisateurs en dur dans une liste (dans `route.py` ou un fichier dédié) | `app/auth/route.py` |
| 1.10 | Créer le blueprint `auth` avec `url_prefix='/auth'` | `app/auth/route.py` |
| 1.11 | Implémenter la route `/auth/login` (GET : formulaire, POST : vérification) | `app/auth/route.py` |
| 1.12 | Implémenter la route `/auth/logout` (vider la session, redirect) | `app/auth/route.py` |
| 1.13 | Créer le template `auth/login.html` qui hérite de `base.html` | `app/templates/auth/login.html` |
| 1.14 | Implémenter le décorateur `login_required` | `app/auth/route.py` |
| 1.15 | Ajouter les flash messages (succès, erreur) | `app/auth/route.py` |
| 1.16 | Enregistrer le blueprint auth dans `create_app()` | **Demander merge Admin** |
| 1.17 | **PR → Admin review → Merge** | — |

### Structure après Phase 1

```
edu-crm/
├── app/
│   ├── __init__.py              ← create_app() avec dashboard_bp + auth_bp
│   ├── config.py
│   ├── run.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── route.py             ← ✅ login, logout, login_required
│   ├── dashboard/
│   │   ├── __init__.py
│   │   └── route.py             ← ✅ route /
│   ├── students/                ← encore vide
│   ├── teachers/                ← encore vide
│   ├── courses/                 ← encore vide
│   ├── services/                ← encore vide
│   └── templates/
│       ├── base.html            ← ✅ navbar + flash + block content
│       ├── auth/
│       │   └── login.html       ← ✅
│       └── dashboard/
│           └── index.html       ← ✅ basique
├── .gitignore
├── requirements.txt
└── README.md
```

### ✅ Point de revue 1

- [ ] La page d'accueil `/` s'affiche avec la navbar
- [ ] On peut se connecter via `/auth/login`
- [ ] On peut se déconnecter via `/auth/logout`
- [ ] Les flash messages s'affichent
- [ ] Les routes non protégées redirigent vers login
- [ ] `base.html` contient la navbar et les blocs nécessaires
- [ ] **Tout le monde fait `git pull origin main` avant de passer à la Phase 2**

---

## PHASE 2 — Modules Students & Teachers (en parallèle)

> Étudiant 2 et Étudiant 3 travaillent **en même temps**, chacun sur son module.  
> Ils ne touchent pas aux mêmes fichiers → pas de conflit.

---

### Étudiant 2 — Module Students

**Branche : `feature/students-crud`**

| # | Tâche | Fichier(s) |
|---|---|---|
| 2.1 | Implémenter `student_service.py` : la liste en mémoire + `add_student()` | `app/services/student_service.py` |
| 2.2 | Implémenter `list_students()` | `app/services/student_service.py` |
| 2.3 | Implémenter `get_student_by_id()` | `app/services/student_service.py` |
| 2.4 | Implémenter `delete_student()` | `app/services/student_service.py` |
| 2.5 | Créer le blueprint `students` avec `url_prefix='/students'` | `app/students/route.py` |
| 2.6 | Route `GET /students` → affiche la liste | `app/students/route.py` |
| 2.7 | Route `GET+POST /students/create` → formulaire + ajout | `app/students/route.py` |
| 2.8 | Route `GET /students/delete/<id>` → supprime + redirect | `app/students/route.py` |
| 2.9 | Protéger les routes avec `@login_required` | `app/students/route.py` |
| 2.10 | Créer `students/list.html` (hérite de base.html) | `app/templates/students/list.html` |
| 2.11 | Créer `students/create.html` | `app/templates/students/create.html` |
| 2.12 | Enregistrer le blueprint dans `create_app()` | **Demander merge Admin** |
| 2.13 | **PR → Admin review → Merge** | — |

---

### Étudiant 3 — Module Teachers

**Branche : `feature/teachers-crud`**

| # | Tâche | Fichier(s) |
|---|---|---|
| 3.1 | Implémenter `teacher_service.py` : la liste en mémoire + `add_teacher()` | `app/services/teacher_service.py` |
| 3.2 | Implémenter `list_teachers()` | `app/services/teacher_service.py` |
| 3.3 | Implémenter `get_teacher_by_id()` | `app/services/teacher_service.py` |
| 3.4 | Implémenter `delete_teacher()` | `app/services/teacher_service.py` |
| 3.5 | Créer le blueprint `teachers` avec `url_prefix='/teachers'` | `app/teachers/route.py` |
| 3.6 | Route `GET /teachers` → affiche la liste | `app/teachers/route.py` |
| 3.7 | Route `GET+POST /teachers/create` → formulaire + ajout | `app/teachers/route.py` |
| 3.8 | Route `GET /teachers/delete/<id>` → supprime + redirect | `app/teachers/route.py` |
| 3.9 | Protéger les routes avec `@login_required` | `app/teachers/route.py` |
| 3.10 | Créer `teachers/list.html` (hérite de base.html) | `app/templates/teachers/list.html` |
| 3.11 | Créer `teachers/create.html` | `app/templates/teachers/create.html` |
| 3.12 | Enregistrer le blueprint dans `create_app()` | **Demander merge Admin** |
| 3.13 | **PR → Admin review → Merge** | — |

### Structure après Phase 2

```
edu-crm/
├── app/
│   ├── __init__.py              ← + students_bp + teachers_bp
│   ├── config.py
│   ├── auth/
│   │   └── route.py             ← ✅
│   ├── dashboard/
│   │   └── route.py             ← ✅
│   ├── students/
│   │   └── route.py             ← ✅ list, create, delete
│   ├── teachers/
│   │   └── route.py             ← ✅ list, create, delete
│   ├── courses/                 ← encore vide
│   ├── services/
│   │   ├── student_service.py   ← ✅ CRUD complet
│   │   ├── teacher_service.py   ← ✅ CRUD complet
│   │   └── course_service.py    ← encore vide
│   └── templates/
│       ├── base.html            ← ✅
│       ├── auth/login.html      ← ✅
│       ├── students/
│       │   ├── list.html        ← ✅
│       │   └── create.html      ← ✅
│       ├── teachers/
│       │   ├── list.html        ← ✅
│       │   └── create.html      ← ✅
│       ├── courses/             ← vide
│       └── dashboard/
│           └── index.html       ← ✅ basique
```

### ✅ Point de revue 2

- [ ] On peut lister, ajouter, supprimer des étudiants
- [ ] On peut lister, ajouter, supprimer des enseignants
- [ ] Les routes sont protégées (redirect si non connecté)
- [ ] La logique est dans les services, PAS dans les routes
- [ ] Les templates héritent de `base.html`
- [ ] Les flash messages fonctionnent
- [ ] **Tout le monde fait `git pull origin main`**

---

## PHASE 3 — Module Courses

> Étudiant 4 commence **après la Phase 2** car il a besoin de `student_service` et `teacher_service`.

### Étudiant 4 — Module Courses

**Branche : `feature/courses-crud`**

| # | Tâche | Fichier(s) |
|---|---|---|
| 4.1 | Implémenter `course_service.py` : liste en mémoire + `add_course()` | `app/services/course_service.py` |
| 4.2 | Implémenter `list_courses()` | `app/services/course_service.py` |
| 4.3 | Implémenter `assign_student_to_course()` | `app/services/course_service.py` |
| 4.4 | Implémenter `delete_course()` | `app/services/course_service.py` |
| 4.5 | Créer le blueprint `courses` avec `url_prefix='/courses'` | `app/courses/route.py` |
| 4.6 | Route `GET /courses` → liste avec nom enseignant + nombre étudiants | `app/courses/route.py` |
| 4.7 | Route `GET+POST /courses/create` → formulaire avec dropdown enseignants | `app/courses/route.py` |
| 4.8 | Route `GET /courses/delete/<id>` → supprime + redirect | `app/courses/route.py` |
| 4.9 | Protéger les routes avec `@login_required` | `app/courses/route.py` |
| 4.10 | Créer `courses/list.html` | `app/templates/courses/list.html` |
| 4.11 | Créer `courses/create.html` (avec select enseignant + select étudiants) | `app/templates/courses/create.html` |
| 4.12 | Enregistrer le blueprint dans `create_app()` | **Demander merge Admin** |
| 4.13 | **PR → Admin review → Merge** | — |

### Structure après Phase 3

```
edu-crm/
├── app/
│   ├── __init__.py              ← + courses_bp (5 blueprints au total)
│   ├── services/
│   │   ├── student_service.py   ← ✅
│   │   ├── teacher_service.py   ← ✅
│   │   └── course_service.py    ← ✅ avec liens vers les 2 autres
│   └── templates/
│       ├── courses/
│       │   ├── list.html        ← ✅
│       │   └── create.html      ← ✅
│       └── ...
```

### ✅ Point de revue 3

- [ ] On peut créer un cours en sélectionnant un enseignant existant
- [ ] On peut assigner des étudiants à un cours
- [ ] La liste des cours affiche le nom de l'enseignant
- [ ] `course_service` utilise correctement `student_service` et `teacher_service`
- [ ] Suppression fonctionnelle
- [ ] **Tout le monde fait `git pull origin main`**

---

## PHASE 4 — Dashboard statistique

### Étudiant 5 — Dashboard complet

**Branche : `feature/dashboard-stats`**

| # | Tâche | Fichier(s) |
|---|---|---|
| 5.1 | Importer les 3 services dans `dashboard/route.py` | `app/dashboard/route.py` |
| 5.2 | Modifier la route `/` pour passer les compteurs au template | `app/dashboard/route.py` |
| 5.3 | Mettre à jour `dashboard/index.html` : afficher nombre d'étudiants, enseignants, cours | `app/templates/dashboard/index.html` |
| 5.4 | Vérifier la cohérence visuelle de tous les templates | Tous les templates |
| 5.5 | Ajuster `base.html` si nécessaire (navbar active, styles) | `app/templates/base.html` |
| 5.6 | **PR → Admin review → Merge** | — |

### ✅ Point de revue 4

- [ ] Le dashboard affiche les 3 compteurs en temps réel
- [ ] La navbar indique la page active
- [ ] L'UI est cohérente sur toutes les pages

---

## PHASE 5 — Intégration finale & tests

**Responsable : Tout le monde, coordonné par l'Admin**  
**Branche : `integration/final-tests`**

| # | Tâche | Qui |
|---|---|---|
| 5.1 | Vérifier que `create_app()` enregistre les 5 blueprints | Admin |
| 5.2 | Tester le parcours complet : login → dashboard → CRUD → logout | Tout le monde |
| 5.3 | Vérifier que les routes protégées redirigent bien | Étudiant 1 |
| 5.4 | Vérifier la cohérence des données entre modules | Étudiant 4 |
| 5.5 | Vérifier l'affichage des flash messages partout | Étudiant 5 |
| 5.6 | Préparer les réponses aux questions obligatoires | Tout le monde |
| 5.7 | Rédiger le README final | Admin |

### Parcours de test complet

```
1. Ouvrir http://127.0.0.1:5000
2. → Redirigé vers /auth/login
3. Se connecter avec les identifiants
4. → Dashboard avec compteurs à 0
5. Aller sur /students → liste vide
6. Créer 2 étudiants → vérifier qu'ils apparaissent
7. Aller sur /teachers → liste vide
8. Créer 1 enseignant → vérifier
9. Aller sur /courses → liste vide
10. Créer 1 cours en sélectionnant l'enseignant
11. Assigner les étudiants au cours
12. Retour Dashboard → compteurs : 2 étudiants, 1 enseignant, 1 cours
13. Supprimer un étudiant → vérifier partout
14. Se déconnecter → retour login
15. Tenter d'accéder à /students → redirigé vers login
```

### ✅ Point de revue final

- [ ] Tout le parcours de test passe
- [ ] Aucune erreur 500
- [ ] Tous les blueprints sont enregistrés
- [ ] Les questions pédagogiques ont été préparées

---

## Conventions de nommage

### Données en mémoire

| Entité | Champs | Exemple |
|---|---|---|
| Student | `id`, `name`, `email` | `{"id": 1, "name": "Awa Diop", "email": "awa@edu.sn"}` |
| Teacher | `id`, `name`, `email`, `speciality` | `{"id": 1, "name": "M. Fall", "email": "fall@edu.sn", "speciality": "Python"}` |
| Course | `id`, `title`, `teacher_id`, `student_ids` | `{"id": 1, "title": "Flask", "teacher_id": 1, "student_ids": [1, 2]}` |

### Fonctions de service

| Service | Fonctions obligatoires |
|---|---|
| `student_service.py` | `add_student(name, email)`, `list_students()`, `get_student_by_id(id)`, `delete_student(id)` |
| `teacher_service.py` | `add_teacher(name, email, speciality)`, `list_teachers()`, `get_teacher_by_id(id)`, `delete_teacher(id)` |
| `course_service.py` | `add_course(title, teacher_id)`, `list_courses()`, `assign_student_to_course(course_id, student_id)`, `delete_course(id)` |

### Noms des Blueprints

| Module | Nom variable | Nom blueprint | Préfixe URL |
|---|---|---|---|
| Auth | `auth_bp` | `'auth'` | `/auth` |
| Students | `students_bp` | `'students'` | `/students` |
| Teachers | `teachers_bp` | `'teachers'` | `/teachers` |
| Courses | `courses_bp` | `'courses'` | `/courses` |
| Dashboard | `dashboard_bp` | `'dashboard'` | `/` |

### Noms des templates

| Template | Chemin |
|---|---|
| Base | `base.html` |
| Login | `auth/login.html` |
| Liste étudiants | `students/list.html` |
| Ajout étudiant | `students/create.html` |
| Liste enseignants | `teachers/list.html` |
| Ajout enseignant | `teachers/create.html` |
| Liste cours | `courses/list.html` |
| Ajout cours | `courses/create.html` |
| Dashboard | `dashboard/index.html` |