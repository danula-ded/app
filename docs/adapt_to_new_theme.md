# Как переделывать проект под другую тему

Этот проект не является универсальным конструктором. Это простой Django-шаблон, который легче переделывать вручную, чем писать с нуля.

Если тема полностью другая, например вместо магазина обуви дали шиномонтажку, думай не про “одно новое поле”, а про замену предметной области.

## Главная Идея

В проекте есть типовая структура:

```text
Role              роли
User              пользователи
Product           главная сущность
Order             заказ / заявка
OrderItem         позиции заказа / заявки
Category          категория
Supplier          поставщик / исполнитель / партнер
Manufacturer      производитель / бренд
Unit              единица измерения
OrderStatus       статус
PickupPoint       пункт выдачи / адрес / место выполнения
```

На экзамене можно оставить технические имена `Product`, `Order`, `OrderItem`, если структура задания похожая. В браузере можно просто заменить текст в HTML.

Если эксперт смотрит код очень внимательно или тема сильно отличается, можно переименовать модели, но это дольше и рискованнее.

## Что Менять В Первую Очередь

### 1. Текст На Страницах

Файлы:

```text
core/templates/core/base.html
core/templates/core/product_list.html
core/templates/core/product_form.html
core/templates/core/product_confirm_delete.html
core/templates/core/order_list.html
core/templates/core/order_form.html
core/templates/core/order_confirm_delete.html
```

Пример:

```text
ООО Обувь -> Шиномонтаж
Товары -> Услуги
Заказы -> Заявки
Добавить товар -> Добавить услугу
```

### 2. Модели И Сущности

Файл:

```text
core/models.py
```

Если новая тема похожая, можно оставить `Product` и `Order`.

Если данные другие, меняешь поля внутри моделей.

Пример для услуги:

```python
class Product(models.Model):
    article = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField()
    photo = models.ImageField(upload_to="products/", null=True, blank=True)
```

То есть можно убрать поля, которые не нужны, и добавить нужные.

После изменения моделей:

```powershell
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### 3. Формы

Файл:

```text
core/forms.py
```

В `ProductForm` меняешь список `fields` и подписи `labels` под новые поля модели.

Если в модели нет `manufacturer`, значит в форме его тоже быть не должно.

### 4. Список И CRUD

Файл:

```text
core/views.py
```

Там меняются:

- `select_related(...)`;
- поля поиска в `Q(...)`;
- сортировка;
- сообщения пользователю.

Пример:

```python
products = products.filter(
    Q(name__icontains=query)
    | Q(description__icontains=query)
    | Q(category__name__icontains=query)
)
```

### 5. HTML Вывод Полей

Файл:

```text
core/templates/core/product_list.html
```

Если в модели нет `manufacturer`, удали:

```html
<dt>Производитель</dt>
<dd>{{ product.manufacturer }}</dd>
```

Если появилось поле `duration`, добавь:

```html
<dt>Длительность</dt>
<dd>{{ product.duration }}</dd>
```

### 6. Импорт Excel

Файл:

```text
core/management/commands/import_data.py
```

Вверху меняешь:

```text
FILES
PRODUCT
USER
ORDER
ROLE_MAP
```

Ниже, в `import_products`, меняешь создание справочников и `defaults`.

Если в новой теме нет производителя, убираешь:

```python
manufacturer, _ = Manufacturer.objects.get_or_create(...)
"manufacturer": manufacturer,
```

Если появилось поле `duration`, добавляешь:

```python
"duration": number(cell(row, PRODUCT["duration"])),
```

## Быстрый Порядок Переделки

```text
1. Прочитать задание.
2. Выписать сущности и поля.
3. Решить: оставляю Product/Order или переименовываю.
4. Поменять models.py.
5. Поменять forms.py.
6. Поменять views.py.
7. Поменять HTML-шаблоны.
8. Поменять import_data.py.
9. Выполнить makemigrations и migrate.
10. Выполнить import_data.
11. Проверить страницы.
```

## Самое Важное

Если предметная область другая, одного файла для замены быть не может.

Минимальный набор файлов для переделки:

```text
core/models.py
core/forms.py
core/views.py
core/management/commands/import_data.py
core/templates/core/product_list.html
core/templates/core/product_form.html
```

Это нормально. Главное - менять их в одном и том же порядке.
