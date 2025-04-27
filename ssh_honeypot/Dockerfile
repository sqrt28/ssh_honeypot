FROM python:3.12-slim

LABEL authors="sqrt28"

# Installer les dépendances système nécessaires pour paramiko
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Définir le dossier de travail
WORKDIR /app

# Copier les fichiers
COPY requirements.txt .
COPY honeypot.py .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel ton honeypot écoute
EXPOSE 2222

# Commande à exécuter
CMD ["python", "honeypot.py"]