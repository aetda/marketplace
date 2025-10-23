# Marketplace API

Django REST API для e-commerce проекта.  

## Структура проекта

- `products/` — каталог с продуктами, категориями, сериализаторами и вьюхами  
- `cart/` — корзина пользователей  
- `ecommerce_api/` — основной проект Django  
- `.venv/` — виртуальное окружение (не в Git)  
- `fixtures.json` — фикстуры для тестовых данных  

## Установка

1. Клонируем репозиторий:

git clone <URL репозитория>
cd marketplace_api

## Создаём виртуальное окружение и активируем его:
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

Устанавливаем зависимости:
pip install -r requirements.txt

## Важная информация

В файле `ecommerce_api/settings.py` значение `SECRET_KEY` нужно генерировать самостоятельно, чтобы проект был безопасным. Для этого можно использовать встроенный модуль Python:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

Скопируйте сгенерированный ключ и вставьте его вместо значения SECRET_KEY в settings.py.

## Делаем миграции и создаём суперпользователя:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

## Запускаем сервер:
python manage.py runserver
API Endpoints

api/products/ — список продуктов
api/cart/ — корзина пользователя
api/token-auth/ — получение токена для аутентификации
api/schema/ — OpenAPI схема
swagger/ — Swagger UI

Для работы с защищёнными эндпоинтами используйте токен авторизации.
## Использование токена
Пример запроса с curl:

curl -X POST http://127.0.0.1:8000/api/token-auth/ \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "password"}'
Ответ:
{
  "token": "your-token-here"
}

## Загрузка фикстур
python manage.py loaddata fixtures.json

Все изменения в БД делайте через миграции

Для тестов используйте фикстуры или создавайте свои объекты через админку.
