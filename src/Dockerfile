# Base cli tool image with all dependencies
FROM niktor99/cli-base-image:latest as final

WORKDIR /app

# Copia SOLO il codice (le dipendenze sono già nell'immagine base)
COPY . ./src/

# Entrypoint specifico
CMD ["python", "src/main.py"]

