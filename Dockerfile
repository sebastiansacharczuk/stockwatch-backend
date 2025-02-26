# Używamy oficjalnego obrazu Pythona jako bazy
FROM python:3.11-slim

# Ustawiamy zmienną środowiskową, aby Python nie buforował wyjścia
ENV PYTHONUNBUFFERED=1

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Instalujemy zależności systemowe potrzebne dla psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiujemy pliki wymagań
COPY requirements.txt .

# Instalujemy zależności Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę kodu aplikacji
COPY . .

# Eksponujemy port (domyślnie 8000 dla Django)
EXPOSE 8000

# Uruchamiamy makemigrations, migrate i serwer
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]