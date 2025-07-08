# Base cli tool image with all dependencies
FROM niktor99/cli-base-image:latest as final

WORKDIR /src

# Copia SOLO il codice (le dipendenze sono già nell'immagine base)
COPY . .

# Entrypoint specifico
CMD ["python", "cli_shell.py"]

