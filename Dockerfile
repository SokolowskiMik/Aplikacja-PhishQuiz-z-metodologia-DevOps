# Używamy wersji 'slim', która jest mniejsza i bezpieczniejsza
FROM python:3.11-slim

# Zapobiega zapisywaniu przez Pythona plików .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Zapobiega buforowaniu outputu, co ułatwia logowanie w Dockerze
ENV PYTHONUNBUFFERED 1

# Krok 3: Stwórz i ustaw katalog roboczy w kontenerze
WORKDIR /app

# Krok 4: Zainstaluj zależności
# Najpierw kopiujemy tylko plik z zależnościami, aby wykorzystać cache Dockera.
# Ten krok zostanie wykonany ponownie tylko, jeśli requirements.txt się zmieni.
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Krok 6 (Opcjonalny, ale zalecany): Stwórz użytkownika bez uprawnień root
RUN addgroup --system app && adduser --system --group app
USER app

# Krok 7: Zdefiniuj domyślną komendę do uruchomienia aplikacji
# Uruchamia serwer Gunicorn, który będzie obsługiwał naszą aplikację Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]