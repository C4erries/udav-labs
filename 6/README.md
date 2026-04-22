# Страховая компания

Сервис для предметной области **«Страховая компания»**.

Что есть внутри:

- SQLite3 база данных с тремя связанными таблицами: `clients`, `policies`, `claims`.
- SQL-скрипты для создания и заполнения БД.
- Веб-сервис с JSON API и HTML-страницами.
- HTML-формы для добавления клиентов, полисов и страховых случаев.
- Экспорт и импорт таблиц через JSON.
- Минимальная DDD-подобная структура без лишнего усложнения.

## Структура

```text
6/
  app/
    domain/          # сущности предметной области
    application/     # сервисы / сценарии приложения
    infrastructure/  # SQLite и репозитории
    web/             # FastAPI routes и Pydantic-схемы
    templates/       # Jinja2 HTML-шаблоны
    static/          # CSS
  data/              # здесь создается insurance.db
  scripts/           # служебные скрипты
  sql/               # schema.sql, seed.sql, statistics.sql
```

## Запуск

Из папки `6`:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

После запуска открыть:

```text
http://127.0.0.1:8000
```

## Инициализация БД вручную

База также создается автоматически при старте приложения. Если нужно создать ее отдельно:

```bash
python scripts/init_db.py
```

## Основные endpoints

HTML:

- `GET /` - главная страница.
- `GET /clients` - клиенты.
- `GET /policies` - полисы.
- `GET /claims` - страховые случаи.
- `GET /statistics` - статистические запросы.
- `GET /clients/new`, `POST /clients/new` - форма добавления клиента.
- `GET /policies/new`, `POST /policies/new` - форма добавления полиса.
- `GET /claims/new`, `POST /claims/new` - форма добавления страхового случая.

JSON API:

- `GET /api/clients`, `POST /api/clients`
- `GET /api/policies`, `POST /api/policies`
- `GET /api/claims`, `POST /api/claims`
- `GET /api/statistics`
- `GET /api/export/{table_name}` - экспорт таблицы в JSON.
- `POST /api/import/{table_name}` - импорт JSON-массива записей.

Для импорта доступны таблицы:

```text
clients
policies
claims
```

Пример экспорта:

```bash
curl http://127.0.0.1:8000/api/export/clients
```

Пример импорта:

```bash
curl -X POST http://127.0.0.1:8000/api/import/clients \
  -H "Content-Type: application/json" \
  -d '[{"full_name":"Новый клиент","phone":"+7 900 000-00-00","email":"new@example.ru","birth_date":"1995-01-01"}]'
```
