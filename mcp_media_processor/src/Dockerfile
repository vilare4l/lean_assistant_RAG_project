# Dockerfile pour les serveurs MCP Python

# Utiliser une image Python de base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Commande pour lancer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
