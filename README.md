# Task Manager API

Асинхронный **Task Manager** на Python с FastAPI и PostgreSQL.  
Проект позволяет создавать, обновлять, удалять и получать задачи через REST API.

---

## 📌 Стек технологий

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker
- Pytest 

---

## 🚀 Быстрый запуск через Docker

1. Клонируем репозиторий:

```bash
git clone https://github.com/Lemingen/TaskManager.git
cd TaskManager
```

2. Поднимаем микросервис

```bash
docker-compose up -d
```

API будет доступен по адресу: http://localhost:8000
Swagger UI: http://localhost:8000/docs

## 🚀 Запуск тестов

1. Заходим в контейнер

```bash
docker exec -it task_manager_back /bin/bash
```

2. Запускаем тесты

```bash
pytest -v
```
