# Python Image
FROM python:3.9

# Setze das Arbeitsverzeichnis
WORKDIR /usr/src/app

# Kopiere requirements und installiere
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Bot Code
COPY . .

# Starte den Bot
CMD ["python", "bot.py"]
