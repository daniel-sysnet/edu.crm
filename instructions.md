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
git clone https://github.com/daniel-sysnet/edu.crm

# 2. Entrer dans le dossier
cd edu-crm

# Ouvrir le projet avec vs code
code .

# Afficher le terminal de vscode
# 3. Créer votre environnement virtuel
python -m venv .venv

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
| `Étudiant-1-Responsable-AUTH-&-Sécurité` | Étudiant 1 |
| `Étudiant-2-Responsable-STUDENTS` | Étudiant 2 |
| `Étudiant-3-Responsable-TEACHERS` | Étudiant 3 |
| `Étudiant-4-Responsable-COURSES` | Étudiant 4 |
| `fÉtudiant-5-Responsable-Dashboard-&-UI` | Étudiant 5 |


### 4.4. Pousser votre branche et créer une Pull Request

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