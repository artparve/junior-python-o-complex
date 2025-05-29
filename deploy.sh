#!/bin/bash
# deploy.sh - Скрипт для развертывания системы

# Проверка наличия Docker и Docker Compose
if ! command -v docker &> /dev/null; then
    echo "Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

ENV_FILE="backend/.env"
API_KEY_VAR="OPEN_WEATHER_API_TOKEN"

# Проверка существования файла
if [[ ! -f "$ENV_FILE" ]]; then
    echo "Файл .env не найден, начинаем создание"
    
    # Интерактивный ввод ключа
    read -p "Введите API ключ OpenWeather: " api_key
    
    # Валидация ввода
    while [[ -z "$api_key" ]]; do
        read -p "Ключ не может быть пустым. Повторите ввод: " api_key
    done
    
    # Создание файла с ключом
    echo "$API_KEY_VAR = '$api_key'" > "$ENV_FILE"
    echo "Файл .env успешно создан"
    
    # Установка прав доступа
    chmod 600 "$ENV_FILE"
else
    # Проверка наличия ключа в существующем файле
    if grep -q "^$API_KEY_VAR = " "$ENV_FILE"; then
        echo "API ключ найден в файле .env"
    else
        echo "Ошибка: Файл существует, но ключ отсутствует" >&2
        exit 1
    fi
fi

sleep 5

# Остановка и удаление существующих контейнеров
echo "Остановка существующих контейнеров..."
docker compose down -v

# Сборка и запуск сервисов
echo "Сборка и запуск сервисов..."
docker compose up --build -d

# Ожидание готовности сервисов
echo "Ожидание готовности сервисов..."
sleep 10

# Проверка состояния сервисов
echo "Проверка состояния сервисов..."
docker compose ps