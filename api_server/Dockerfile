FROM niktor99/api-base:latest as final

WORKDIR /app/api_server

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "entrypoint.py"]
