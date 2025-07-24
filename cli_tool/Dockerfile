FROM python:3.10

WORKDIR /app/cli_tool

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Entrypoint specifico
CMD ["python", "cli_shell.py"]

