# Страховая компания

Сайт для предметной области **«Страховая компания»**.

## Что реализовано

- Модели `Client`, `InsuranceProduct`, `Policy`, `Claim`.
- Связи между таблицами: клиент → полисы, продукт → полисы, полис → страховые случаи.
- Админ-панель с `list_display`, `list_filter`, `search_fields`, `date_hierarchy`.
- Главная страница со списком всех полисов в краткой форме.
- Детальная страница полиса.
- Создание и редактирование клиентов, продуктов, полисов и страховых случаев через клиентскую часть.
- SQLite база данных.
- Команда для заполнения демо-данными.

## Запуск

Из папки `7`:

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Открыть сайт:

```text
http://127.0.0.1:8000/
```

Админка:

```text
http://127.0.0.1:8000/admin/
```

Создать администратора:

```bash
python manage.py createsuperuser
```

## Основные страницы

- `/` - главная страница со всеми полисами.
- `/policies/<id>/` - детальная страница полиса.
- `/policies/new/` - создание полиса.
- `/policies/<id>/edit/` - редактирование полиса.
- `/clients/`, `/clients/new/`, `/clients/<id>/edit/` - клиенты.
- `/products/`, `/products/new/`, `/products/<id>/edit/` - страховые продукты.
- `/claims/`, `/claims/new/`, `/claims/<id>/edit/` - страховые случаи.
