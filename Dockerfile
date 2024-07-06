# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Копируем исходный код приложения в Docker-образ
COPY . /app
WORKDIR /app

# Запускаем приложение
CMD ["flask", "run", "--host=0.0.0.0"]
