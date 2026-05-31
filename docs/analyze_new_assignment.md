# Как разбирать новый вариант задания

Этот файл нужен для случаев, когда меняется не только тема, а вся предметная область.

Пример: в одном году магазин обуви, в другом - производственная компания и партнеры. В такой ситуации нельзя просто заменить слова в HTML. Нужно сначала разобрать задание, а потом менять модели, формы, импорт и страницы.

## 1. Сначала Выпиши 5 Вещей

Перед кодом сделай короткую таблицу:

```text
1. Главная сущность:
2. Какие страницы нужны:
3. Какие формы нужны:
4. Какие Excel-файлы дали:
5. Какие формулы/расчеты требуются:
```

Пример для задания с партнерами:

```text
Главная сущность: Partner
Страницы: список партнеров, форма партнера, история продаж партнера
Формы: добавление/редактирование партнера
Excel: partners, products, product types, material types, partner products
Формулы: скидка партнера, расчет материала
```

## 2. Сравни С Нашим Шаблоном

Наш шаблон уже умеет:

- подключаться к PostgreSQL;
- делать миграции;
- читать Excel через management command;
- показывать список;
- делать добавление/редактирование/удаление;
- показывать связанную таблицу;
- работать с формами;
- отдавать статику и медиа;
- хранить документы и команды запуска.

Но названия сущностей могут быть другими.

## 3. Если Сущности Другие

Меняй файлы в таком порядке:

```text
core/models.py
core/forms.py
core/views.py
config/urls.py
core/templates/core/
core/management/commands/import_data.py
```

Не начинай с HTML. Сначала база данных.

## 4. Как Понять Какие Модели Нужны

Смотри на Excel-файлы и связи.

Если дали файл `Partners_import.xlsx`, почти точно нужна модель:

```python
class Partner(models.Model):
    ...
```

Если дали файл `Product_type_import.xlsx`, нужна справочная модель:

```python
class ProductType(models.Model):
    ...
```

Если дали файл, где есть и партнер, и продукт, это таблица связи/истории:

```python
class PartnerProduct(models.Model):
    partner = models.ForeignKey(Partner, ...)
    product = models.ForeignKey(Product, ...)
    quantity = models.IntegerField()
    sale_date = models.DateField()
```

## 5. Типовая Схема Для Задания С Партнерами

Это не надо слепо копировать в любой год, но это хороший пример мышления:

```text
PartnerType
Partner
ProductType
Product
MaterialType
PartnerProduct
```

Связи:

```text
Partner.type -> PartnerType
Product.type -> ProductType
PartnerProduct.partner -> Partner
PartnerProduct.product -> Product
```

## 6. Где Делать Формулы

Если в задании есть расчет скидки или материала, не смешивай это с HTML.

Простой вариант:

```text
core/utils.py
```

Примеры функций:

```python
def get_partner_discount(total_quantity):
    ...

def calculate_material(product_type_id, material_type_id, quantity, param1, param2):
    ...
```

Потом вызывай функцию во `views.py` или в свойстве модели.

## 7. Как Переписать Импорт

Файл:

```text
core/management/commands/import_data.py
```

Для каждого Excel делай отдельный метод:

```python
def import_partners(self, folder):
    ...

def import_products(self, folder):
    ...

def import_partner_products(self, folder):
    ...
```

Порядок импорта всегда такой:

```text
1. Справочники
2. Главные сущности
3. Связанные/исторические таблицы
```

Для партнеров:

```text
1. ProductType
2. MaterialType
3. Product
4. PartnerType / Partner
5. PartnerProduct
```

## 8. Как Быстро Проверить Что Ты На Правильном Пути

После `import_data` проверь количество записей:

```powershell
uv run python manage.py shell -c "from core.models import Partner, Product; print(Partner.objects.count(), Product.objects.count())"
```

Если импорт упал, сначала смотри:

```text
название Excel-файла
номер колонки
порядок импорта
ForeignKey, который еще не создан
```

## 9. Главное Правило

Если задание другого года выглядит совсем иначе, не пытайся натянуть его на старые `Product` и `Order`.

Используй старый проект как каркас Django:

```text
настройки
команды
структура папок
шаблоны
примеры ListView/CreateView/UpdateView
пример import_data
```

А предметные модели пиши под новое задание.
