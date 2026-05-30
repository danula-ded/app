# План истории коммитов

Такую историю удобно повторить на экзамене, если можно клонировать репозиторий и показывать этапы работы.

## Рекомендуемые коммиты

1. `init django project`

   Проект Django, `pyproject.toml`, `uv.lock`, `manage.py`, настройки, статика.

2. `add database models and import command`

   Модели, миграции, PostgreSQL, команда `import_data`, Excel-файлы.

3. `add login and product catalog`

   Авторизация, вход гостем, список товаров, фото, заглушка, цвета по условию.

4. `add product crud and role permissions`

   Поиск, фильтр, сортировка, формы товара, CSRF, права администратора.

5. `add orders module`

   Список заказов, добавление, редактирование, удаление, разбор строки артикулов.

6. `add media validation and maintenance`

   Pillow, сжатие фото, удаление старых изображений.

7. `add exam documentation`

   README, алгоритм модуля 2, блок-схема PDF, инструкция запуска.

## Команды

```powershell
git add .
git commit -m "add full demo exam solution"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

Если хочется делать историю строго по этапам, после каждого завершенного модуля выполняй:

```powershell
git add .
git commit -m "module 1 database and import"
```

Главное: не коммить `.venv`, временные логи и локальные пароли вне `settings.py`, если преподаватель не требует именно такой формат.
