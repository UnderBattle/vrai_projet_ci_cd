# Image de base officielle et allégée
FROM python:3.11-slim

# Défini le dossier de travail
WORKDIR /code

# Optimisation du cache Docker
COPY ./requirements.txt /code/requirements.txt

# Installation des dépendances
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# On copie le reste du code (le dossier "app")
COPY ./app /code/app

# On expose le port sur lequel FastAPI va tourner
EXPOSE 8000

# La commande pour lancer le serveur
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]