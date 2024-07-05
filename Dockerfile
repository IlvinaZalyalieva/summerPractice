# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем psycopg2 (драйвер PostgreSQL для Python)
RUN pip install --no-cache-dir psycopg2-binary Flask 
RUN pip install requests
# Копируем исходный код приложения в Docker-образ
COPY . /app
WORKDIR /app

# Запускаем приложение
CMD ["flask", "run", "--host=0.0.0.0"]
