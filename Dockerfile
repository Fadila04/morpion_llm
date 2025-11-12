# 1 : image Python légère
FROM python:3.12-slim

# 2 : répertoire de travail
WORKDIR /app

# 3 : copier les dépendances et les installer
COPY requirements.txt .

# 4 Installer curl
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# 5 Installer Ollama via script officiel

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 6. Ajouter le dossier racine au PYTHONPATH
ENV PYTHONPATH="/backend"

# 8. Exposer le port du conteneur
EXPOSE 8000

# 9. Lancer l’application Streamlit
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8001"]