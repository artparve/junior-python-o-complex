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