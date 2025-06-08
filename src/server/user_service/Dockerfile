# Bazowy obraz: Python na Alpine (lekki)
FROM python:3.13-alpine

# Ustawienie katalogu roboczego
WORKDIR /app

# Zainstaluj narzędzia systemowe i zależności do budowania pakietów Pythonowych
RUN apk add --no-cache gcc musl-dev libffi-dev netcat-openbsd

# Skopiuj plik z zależnościami
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały kod źródłowy aplikacji
COPY . .

# Skopiuj i nadaj prawa do skryptu entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Ustaw skrypt startowy jako punkt wejścia
ENTRYPOINT ["/entrypoint.sh"]

# Udostępnij port aplikacji
EXPOSE 8001
