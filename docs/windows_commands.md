# Команды Windows для демоэкзамена

Все команды выполнять в PowerShell.

## 1. Перейти в проект

```powershell
cd "C:\Users\Даниил\Desktop\prepare for demo\exam_training_pack\04_your_work_here\project\demoexam_26"
```

## 2. Установить зависимости

```powershell
uv sync
```

Если добавляешь библиотеку:

```powershell
uv add openpyxl
uv add pillow
uv add psycopg2-binary
```

## 3. PostgreSQL на Windows

Найти службу PostgreSQL:

```powershell
Get-Service | Where-Object { $_.Name -like "*postgres*" }
```

Запустить службу, если она остановлена:

```powershell
Start-Service postgresql-x64-17
```

Если имя службы другое, возьми его из предыдущей команды.

Создать базу через `psql`, если не создаешь ее через DBeaver:

```powershell
psql -U postgres -c "CREATE DATABASE demoexam_26;"
```

## 4. Django и база данных

```powershell
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py import_data
```

Проверить проект:

```powershell
uv run python manage.py check
```

## 5. Запуск сайта

```powershell
uv run python manage.py runserver
```

Открыть:

```text
http://127.0.0.1:8000/
```

Если порт 8000 занят:

```powershell
uv run python manage.py runserver 127.0.0.1:8001
```

## 6. Проверить количество данных

```powershell
uv run python manage.py shell -c "from core.models import Product, Order, OrderItem, User; print(Product.objects.count(), Order.objects.count(), OrderItem.objects.count(), User.objects.count())"
```

## 7. Git

```powershell
git status
git add .
git commit -m "add demo exam solution"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

Если remote уже есть:

```powershell
git remote -v
git remote set-url origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

## 8. Главные файлы для изменения

```text
core/exam_config.py       - тема сайта, роли, поля поиска, сортировки
core/management/commands/import_data.py - Excel-файлы и номера колонок
core/models.py            - таблицы БД
core/forms.py             - формы добавления/редактирования
core/views.py             - страницы и права доступа
core/templates/core/      - HTML
static/css/style.css      - стили
```

## 9. Если поменялась тема задания

Например, вместо обуви дали шиномонтажку.

Сначала открыть:

```text
core/exam_config.py
```

Поменять:

```text
APP_TEXT - видимые названия сайта, кнопок и страниц
```

Потом открыть:

```text
core/management/commands/import_data.py
```

В верхнем блоке поменять:

```text
FILES   - названия Excel-файлов
PRODUCT - номера колонок главной сущности
ORDER   - номера колонок заказов/заявок
USER    - номера колонок пользователей
```

Подробная инструкция:

```text
docs/adapt_to_new_theme.md
```
