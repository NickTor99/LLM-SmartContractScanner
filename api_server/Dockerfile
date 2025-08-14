FROM niktor99/api-base-image:latest as final

WORKDIR /app/api_server

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "entrypoint.py"]
