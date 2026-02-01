# Test Chats Dj Api

Тестовый  проект   Django REST Framework проект для чата и сообщений с использованием PostgreSQL и Docker.

---

## Описание

Проект реализует API для создания, получения и удаления чата и сообщений.  
Использует Django + DRF + PostgreSQL в Docker-контейнерах.

---

## Стек технологий

- Python 3.12
- Django 4.2
- Django REST Framework
- PostgreSQL 15
- Gunicorn
- Docker, Docker Compose

---

## Структура проекта

```
app/
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── chats/
│   ├── migrations/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_chat_api.py
│   │   ├── test_messages_api.py
│   │   └── test_serializers.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   └── views.py
└── manage.py
```

---

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/D-Danis/test_chats_dj_api.git
```

`

### 2. Запустить с Docker

> Для запуска проекта необходимы [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).


```bash
docker-compose up --build
```

- Это соберёт образы, поднимет PostgreSQL и Django сервер.
- После успешного запуска сервер будет доступен по адресу: [http://localhost:8000](http://localhost:8000)
- Миграции будут применены автоматически при запуске.

### 3. Запуск тестов

Чтобы выполнить тесты, используйте команду:

```bash
docker compose run --rm web pytest chats/tests/test_*.py -qv
```

- Тест проверяет сериализация данных для Chat и Message
- Тест проверяет CRUD операции для Chat
- Тест проверяет CRUD операции для Message


## Работа с API

### CRUD операции по чату  
- `GET/chats/` получить список чата
```bash
curl --location --request GET 'http://localhost:8000/chats/' \
--header 'Content-Type: application/json' 
```

- `POST/chats/` создание чата
```bash
curl --location 'http://localhost:8000/chats/1/messages/' \
--header 'Content-Type: application/json' \
--data '{"title": "The Chat"}'
```

- `PUT/chats/{pk}/` обновление чата
```bash
curl --location --request PUT 'http://localhost:8000/chats/1/' \
--header 'Content-Type: application/json' \
--data '{"title": "The Update Chat"}'
```

- `DELETE/chats/{pk}/` удаление чата
```bash
curl --location --request DELETE 'http://localhost:8000/chats/1/' \
--header 'Content-Type: application/json
```


### CRUD операции по сообщениям

- `GET/chats/{pk}/messages/` получить список сообщений
```bash
curl --location --request GET 'http://localhost:8000/chats/1/messages/' \
--header 'Content-Type: application/json'
```

- `POST/chats/{pk}/messages/` создание сообщений
```bash
curl --location 'http://localhost:8000/chats/1/messages/' \
--header 'Content-Type: application/json' \
--data '{"text": "The Message"}'
```

- `PUT/chats/{pk}/messages/{pk}/` обновление сообщений
```bash
curl --location --request PUT 'http://localhost:8000/chats/1/messages/' \
--header 'Content-Type: application/json' \
--data '{"text": "The Update Message"}'
```

- `DELETE/chats/{pk}/messages/{pk}/` удаление сообщений
```bash
curl --location --request DELETE 'http://localhost:8000/chats/1/messages/' \
--header 'Content-Type: application/json
```



---

