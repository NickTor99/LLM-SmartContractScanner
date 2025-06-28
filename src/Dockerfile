# Fase builder
FROM python:3.11 as builder
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Fase finale
FROM python:3.11-slim
ENV PATH="/root/.local/bin:${PATH}"
COPY --from=builder /root/.local /root/.local
WORKDIR /src
COPY . .

CMD ["python", "main.py"]
