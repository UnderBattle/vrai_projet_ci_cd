# Projet CI/CD : API To-Do List (Python & Docker)

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![CI/CD Status](https://github.com/UnderBattle/vrai_projet_ci_cd/actions/workflows/ci-cd.yml/badge.svg)

Bienvenue sur le dépôt de notre projet d'INFO0913 sur le pipeline CI/CD.
Ce projet montre la mise en place d'une chaîne d'intégration et de déploiement continus complète, de l'écriture du code jusqu'à la publication d'une image Docker prête pour la production.



---

## Architecture du Pipeline CI/CD (Les 4 Phases)

Notre pipeline automatisé (via **GitHub Actions**) s'exécute à chaque `git push` sur la branche principale et respecte la règle du **"Fail Fast"**.

1. **Phase Source :** Gestion du code via Git et GitHub. Seul le code source est versionné, les environnements virtuels et bases de données locales sont ignorés (`.gitignore`).
2. **Phase Test :** - **Linting :** L'outil `Ruff` vérifie que le code respecte les standards (PEP 8) et bloque le pipeline en cas d'erreur de syntaxe.
   - **Tests Unitaires :** `Pytest` lance une série de tests (CRUD complet) sur une base de données SQLite éphémère (`test.db`) recréée à chaque exécution.
3. **Phase Build :** Si les tests sont au vert, création d'une image Docker isolée et allégée (basée sur `python:3.11-slim`) contenant l'API FastAPI et ses dépendances.
4. **Phase Deploy :** L'image Docker validée est automatiquement poussée sur **Docker Hub** avec le tag `latest`, prête à être téléchargée sur n'importe quel serveur.

---

## Fonctionnalités de l'Application

Il s'agit d'une simple API qui permet de créer une To-Do-List :
- **Backend :** FastAPI avec validation de données stricte via Pydantic V2.
- **Base de données :** SQLite (via SQLAlchemy).
- **Frontend :** Interface Web HTML
- **CRUD Complet :** Création, Lecture, Mise à jour et Suppression de tâches.

---

## Guide Rapide

Vous n'avez pas besoin d'installer Python pour tester ce projet si Docker est installé sur votre machine, ouvrez simplement votre terminal :

```bash
docker run -d -p 8000:8000 underbattle/mon-api-todo:latest
```

Ouvrez ensuite votre navigateur et allez sur :
- **L'application Web :** http://localhost:8000
- **La documentation de l'API :** http://localhost:8000/docs

---

## Guide Développeur (Installation locale)

Si vous souhaitez modifier le code ou contribuer au projet, voici comment installer l'environnement de développement complet.

### 1. Cloner le projet
```bash
git clone [https://github.com/UnderBattle/vrai_projet_ci_cd.git](https://github.com/UnderBattle/vrai_projet_ci_cd.git)
cd vrai_projet_ci_cd
```

### 2. Créer l'environnement virtuel
Pour ne pas polluer votre système, isolez les dépendances :
```bash
# Création
python -m venv .venv

# Activation sur Linux/Mac :
source .venv/bin/activate
# Activation sur Windows :
.venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer le serveur de développement
```bash
uvicorn app.main:app --reload
```
Le serveur redémarrera automatiquement à chaque modification de fichier. Vous pouvez le visualiser sur http://127.0.0.1:8000.

---

## Tests & Qualité de code

**Attention :** Le pipeline GitHub Actions bloquera tout déploiement si ces commandes échouent. Pensez à les lancer en local avant votre `git push` !

**Vérifier la propreté du code :**
```bash
ruff check .
```

**Lancer les tests de l'API :**
```bash
pytest
```
*(L'outil Pytest se chargera de créer et détruire la base de données de test automatiquement).*
