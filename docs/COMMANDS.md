# Команды

## Установка

```powershell
cd "C:\Users\Даниил\Desktop\test demo\app"
uv sync
```

## Проверка проекта

```powershell
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
```

## Миграции

```powershell
uv run python manage.py makemigrations
uv run python manage.py migrate
```

## Импорт

```powershell
uv run python manage.py import_data
```

## Количество данных

```powershell
uv run python manage.py shell -c "from core.models import Product, Order, OrderItem, User, PickupPoint; print(Product.objects.count(), Order.objects.count(), OrderItem.objects.count(), User.objects.count(), PickupPoint.objects.count())"
```

## Запуск

```powershell
uv run python manage.py runserver
```

## SQL

```powershell
uv run python manage.py sqlmigrate core 0001 > schema.sql
```

## Пользователь администратора

```powershell
uv run python manage.py createsuperuser
```

## Git

```powershell
git status
git add .
git commit -m "add project"
git push
```
