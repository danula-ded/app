# Последовательность действий на экзамене

Цель: не написать идеальный проект, а быстро получить рабочий проект, который закрывает требования.

Команды лежат здесь:

```text
docs/windows_commands.md
```

Если задание выглядит сильно иначе, сначала открой:

```text
docs/analyze_new_assignment.md
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
Формулы/расчеты
История/детальная страница
```

Если тема похожая, не переименовывай весь проект. Оставь внутренние `Product` и `Order`, а видимые названия поменяй в HTML.

## 3. Переделать предметную область

Если сущности почти такие же, можно ограничиться текстом и импортом.

Если сущности другие, меняй файлы в таком порядке:

```text
core/models.py
core/forms.py
core/views.py
core/templates/core/
core/management/commands/import_data.py
```

Для текста на страницах чаще всего нужны:

```text
core/templates/core/base.html
core/templates/core/product_list.html
core/templates/core/product_form.html
core/templates/core/order_list.html
core/templates/core/order_form.html
```

Если дали шиномонтажку, меняешь `Товары` на `Услуги`, `Заказы` на `Заявки`.

## 4. Проверить модели

Файл:

```text
core/models.py
```

Если структура похожая, модели можно почти не трогать.

Если сущности другие, переписываешь поля моделей под новые Excel-файлы и связи.

После изменения моделей:

```powershell
uv run python manage.py makemigrations
uv run python manage.py migrate
```

## 5. Настроить импорт Excel

Файл:

```text
core/management/commands/import_data.py
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
docs/how_to_make_gost_algorithm.md
docs/debug_report.docx или скриншоты
```

SQL-скрипт, ER-диаграмму и PDF с блок-схемой делай отдельно на экзамене: SQL/ER через DBeaver, блок-схему по инструкции `docs/how_to_make_gost_algorithm.md`.

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
