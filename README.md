# Referral System API

Этот проект представляет собой RESTful API для реферальной системы, разработанный с использованием **FastAPI**. Он поддерживает регистрацию и аутентификацию пользователей, создание и удаление реферальных кодов, а также управление рефералами.

## Функциональные возможности

- Регистрация и аутентификация пользователей (JWT, OAuth 2.0)
- Создание и удаление реферальных кодов с указанием срока действия
- Возможность регистрации по реферальному коду в качестве реферала
- Получение информации о рефералах по ID реферера
- UI-документация с использованием Swagger и ReDoc

## Технологии

- **Python** 3.11+
- **CI/CD**
- **FastAPI** - фреймворк для создания веб-приложений
- **SQLite** - база данных для хранения данных
- **SQLAlchemy** - ORM для работы с базой данных
- **JWT** - аутентификация и авторизация
- **Pytest** - тестирование

## Установка и запуск

### 1. Установка и запуск referral-system

```bash
git clone https://github.com/Vud18/referral-system.git
```

2. Создание виртуального окружения и установка зависимостей

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```
3. Установите [poetry](https://python-poetry.org/docs/#installation):
```bash
pip install poetry
```
4. Перейдите в директорию `/backend`:
```bash
cd backend
```
5. Установите зависимости
```bash
poetry install
```
6. Настройка базы данных(миграции)
```bash
alembic upgrade head
```
7. Запуск приложения
```bash
uvicorn src.main:app --reload
```
8. Локальный адрес:
```bash
http://127.0.0.1:8000/docs
```

## Тестирование

1. Запуск тестов делаем из \referral-system
```bash
pytest
```