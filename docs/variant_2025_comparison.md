# Сравнение с вариантом 2025

Файл основан на варианте из папки `test demo`. Это не инструкция "сделай именно 2025", а пример того, насколько сильно может поменяться задание.

## Что В 2026 Шаблоне

Текущий шаблон сделан под типовую структуру:

```text
товары
пользователи
роли
заказы
позиции заказов
поиск / фильтр / сортировка
CRUD товаров
CRUD заказов
изображения товаров
```

## Что Было В 2025

Предметная область:

```text
производственная компания
партнеры
продукция
типы продукции
типы материалов
история реализации продукции партнером
```

Excel-файлы:

```text
Partners_import.xlsx
Products_import.xlsx
Product_type_import.xlsx
Material_type_import.xlsx
Partner_products_import.xlsx
```

Страницы:

```text
список партнеров
добавление/редактирование партнера
история продаж конкретного партнера
```

Формулы:

```text
индивидуальная скидка партнера
расчет количества материала
```

## Главное Отличие

Это не просто "обувь поменяли на другое".

В 2025:

- нет такого же каталога товаров, как в шаблоне 2026;
- главная сущность - партнер, а не товар;
- нужен расчет скидки по сумме продаж;
- нужна страница истории продаж партнера;
- нужен отдельный метод расчета материала;
- Excel-файлов 5, а не 4;
- таблицы БД другие.

## Какие Модели Бы Понадобились

Примерная схема:

```text
PartnerType
Partner
ProductType
Product
MaterialType
PartnerProduct
```

Пример полей:

```text
Partner:
type, name, director, email, phone, address, inn, rating

Product:
type, name, article, min_price

ProductType:
name, coefficient

MaterialType:
name, defect_percent

PartnerProduct:
product, partner, quantity, sale_date
```

## Что Можно Взять Из Нашего Шаблона

Полезно оставить:

```text
config/settings.py
config/urls.py как пример
static/css/style.css как основу
base.html как основу
forms.py как пример ModelForm
views.py как пример ListView/CreateView/UpdateView
import_data.py как пример чтения Excel
docs/windows_commands.md
docs/how_to_make_gost_algorithm.md
```

Но придется переписать:

```text
core/models.py
core/forms.py
core/views.py
core/templates/core/product_list.html
core/templates/core/product_form.html
core/management/commands/import_data.py
config/urls.py
```

## Как Действовать Если Попадется Похожий Вариант

1. Не начинай с верстки.
2. Выпиши Excel-файлы.
3. По Excel-файлам выпиши модели.
4. Создай модели и связи.
5. Сделай миграции.
6. Напиши импорт в правильном порядке.
7. Сделай список главной сущности.
8. Сделай форму добавления/редактирования.
9. Сделай страницу истории/деталей, если требуется.
10. Добавь формулу отдельной функцией.
11. Проверь запуск.

## Вывод

Наш шаблон не должен быть "проектом на все годы".

Он должен быть стартовой базой:

```text
Django уже настроен
PostgreSQL уже настроен
есть примеры форм и views
есть пример import_data
есть команды и гайды
```

А новые сущности надо спокойно переписывать под конкретный вариант.
