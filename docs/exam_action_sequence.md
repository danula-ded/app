# Последовательность действий на экзамене

Цель: не написать идеальный проект, а быстро получить рабочий проект, который закрывает требования.

Команды лежат здесь:

```text
docs/windows_commands.md
```

## 1. Развернуть проект

```powershell
uv sync
```

Проверить, что проект живой:

```powershell
uv run python manage.py check
```

## 2. Прочитать задание и выписать сущности

Прямо на листе или в черновике:

```text
Роль
Пользователь
Главная сущность: товар / услуга / материал
Заказ / заявка
Позиция заказа
Справочники: категория, поставщик, статус, пункт выдачи
```

Если тема похожая, не переименовывай весь проект. Оставь внутренние `Product` и `Order`, а видимые названия поменяй позже.

## 3. Настроить видимый текст

Файл:

```text
core/exam_config.py
```

Менять в первую очередь:

```text
APP_TEXT
ADMIN_ROLES
MANAGER_ROLES
PRODUCT_SEARCH_FIELDS
PRODUCT_SORTS
```

Если дали шиномонтажку, меняешь `Товары` на `Услуги`, `Заказы` на `Заявки`.

## 4. Проверить модели

Файл:

```text
core/models.py
```

Если структура похожая, модели можно почти не трогать.

Если появились новые обязательные поля, добавляешь их в модель и потом делаешь:

```powershell
uv run python manage.py makemigrations
uv run python manage.py migrate
```

## 5. Настроить импорт Excel

Файл:

```text
core/management/commands/import_data.py
```

В самом верху есть блок:

```text
МЕНЯТЬ ТОЛЬКО ЭТОТ БЛОК
```

Там меняешь:

```text
FILES   - названия Excel-файлов
PRODUCT - номера колонок главной сущности
USER    - номера колонок пользователей
ORDER   - номера колонок заказов/заявок
ROLE_MAP - роли из Excel
```

Запуск:

```powershell
uv run python manage.py import_data
```

Если один Excel-файл отсутствует, команда просто пропустит его.

## 6. Проверить данные

```powershell
uv run python manage.py shell -c "from core.models import Product, Order, OrderItem, User; print(Product.objects.count(), Order.objects.count(), OrderItem.objects.count(), User.objects.count())"
```

Если числа больше нуля, импорт уже можно показывать как результат вариативной части.

## 7. Проверить страницы

```powershell
uv run python manage.py runserver
```

Открыть:

```text
http://127.0.0.1:8000/
```

Проверить:

```text
/products/
/orders/
/products/add/
/orders/add/
```

## 8. Проверить роли

Администратор:

```text
видит добавление, редактирование, удаление
```

Менеджер:

```text
видит поиск, фильтр, сортировку, заказы
не может добавлять и удалять
```

Клиент и гость:

```text
только просмотр
```

## 9. Проверить медиа

У товара должно быть:

```text
фото из media/products/
или заглушка из static/images/picture.png
```

При загрузке нового фото Pillow сжимает его до 300x200.

## 10. Подготовить файлы для сдачи

Минимально нужны:

```text
исходный код проекта
uv.lock или requirements.txt
docs/database_schema.sql
docs/er_diagram.pdf
docs/universal_development_algorithm_gost.pdf
docs/debug_report.docx или скриншоты
```

## 11. Git

```powershell
git status
git add .
git commit -m "add demo exam project"
git push
```

Если репозиторий новый, команды лежат в:

```text
docs/windows_commands.md
```
