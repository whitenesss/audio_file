#!/usr/bin/env bash
set -e

export ENVIRONMENT=local
export PYTHONDONTWRITEBYTECODE=1

# Путь к основному .env файлу
MAIN_ENV=.env
TEMPLATE_ENV=.env.example

# Проверка наличия необходимых файлов
required_files=("alembic.ini" "src/main.py")
for file in "${required_files[@]}"; do
    if [[ ! -f $file ]]; then
        echo "❌ Отсутствует обязательный файл: $file"
        exit 1
    fi
done

# Создаем .env из примера если отсутствует
if [[ ! -f ${MAIN_ENV} ]]; then
    if [[ -f ${TEMPLATE_ENV} ]]; then
        cp "${TEMPLATE_ENV}" "${MAIN_ENV}"
        echo "✅ Создан ${MAIN_ENV} из шаблона"
    else
        echo "❌ Отсутствует ${MAIN_ENV} и шаблон ${TEMPLATE_ENV}"
        exit 1
    fi
fi

# Запуск контейнеров с автоматическим выполнением миграций
echo "🚀 Запуск Docker-сервисов..."
docker-compose up --build --detach

echo -e "\n⏳ Ожидание инициализации БД и выполнения миграций..."
docker-compose logs -f app | grep -q "Application startup complete"

echo -e "\n✅ Все компоненты запущены!\nДоступные сервисы:"
echo "• FastAPI: http://localhost:8000/docs"
echo "• PostgreSQL: localhost:5432"
echo "• Просмотр логов: docker-compose logs -f"

# Опционально: автоматическое открытие документации в браузере
if command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:8000/docs"
elif command -v open &> /dev/null; then
    open "http://localhost:8000/docs"
fi