FROM python:3.12.8-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Копирование только файлов зависимостей


# Установка зависимостей


# Копирование всего проекта
COPY . .

# Установка корневого пакета


ENV PYTHONPATH=/app/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]