# Инструмент tools

## Установка

```powershell
cd "C:\Users\Даниил\Desktop\test demo\app\tools"
uv sync
```

## Настройка

Заполнить:

```text
tools/local_config.json
```

Минимальный вид:

```json
{
  "YC_API_KEY": "ключ",
  "YC_FOLDER_ID": "folder_id",
  "YC_API_MODE": "sdk",
  "YC_MODEL": "yandexgpt",
  "YC_MODEL_VERSION": "rc",
  "YC_TEMPERATURE": "0.2"
}
```

Файлы задания, Excel и картинки можно класть в:

```text
tools/input/
```

## Команды

```powershell
uv run python tool.py collect
uv run python tool.py test
uv run python tool.py plan
uv run python tool.py schema
uv run python tool.py interface
uv run python tool.py apply
uv run python tool.py ask "вопрос"
uv run python tool.py chat
uv run python tool.py audit
uv run python tool.py audit "что проверить"
uv run python tool.py restore
uv run python tool.py restore 20260531_145542
uv run python tool.py check
uv run python tool.py test_pages
uv run python tool.py repair
```

## Что делает каждая команда

`collect` - собирает контекст проекта и файлов из `tools/input/`.

`test` - проверяет, что настройки в `local_config.json` работают.

`plan` - создает план изменений без правки проекта.

`schema` - меняет только схему: `core/models.py`, `core/admin.py`, `core/management/commands/import_data.py`.

`interface` - меняет интерфейс: формы, views, urls, templates, css, permissions.

`apply` - пытается адаптировать проект целиком и перед записью делает backup.

`ask` - задает один вопрос и ничего не меняет в проекте.

`chat` - открывает диалоговый режим; выход командой `exit`.

`audit` - проверяет соответствие проекта заданию без изменения файлов.

`restore` - восстанавливает файлы из последнего backup.

`restore <имя_backup>` - восстанавливает конкретный backup из `tools/backups/`.

`check` - запускает внутреннюю проверку проекта и сохраняет отчет.

`test_pages` - проверяет страницы через Django test client.

`repair` - пытается исправить проект, если `check` нашел ошибку.

## Ask

`ask` удобен, когда нужно быстро спросить про ошибку, файл или конкретное требование, но не хочется автоматически менять проект.

Примеры:

```powershell
uv run python tool.py ask "Почему migrate падает?"
uv run python tool.py ask "Посмотри core/models.py и core/forms.py. Почему форма товара не сохраняется?"
uv run python tool.py ask "Посмотри config/urls.py и core/views.py. Почему страница заказов не открывается?"
uv run python tool.py ask "Проверь, какие поля нужно поменять под магазин спортинвентаря"
uv run python tool.py ask "Прочитай tools/output/manual_check.md и объясни ошибки"
```

Если в вопросе указать имя файла, инструмент попробует прочитать этот файл и приложить его к вопросу:

```text
core/models.py
core/forms.py
core/views.py
config/urls.py
core/management/commands/import_data.py
tools/output/manual_check.md
```

`ask` не записывает файлы. Для автоматических изменений используются `schema`, `interface`, `apply` или `repair`.

## Обычная последовательность

```powershell
cd "C:\Users\Даниил\Desktop\test demo\app\tools"
uv sync
uv run python tool.py collect
uv run python tool.py plan
uv run python tool.py schema
cd ..
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py import_data
cd tools
uv run python tool.py interface
uv run python tool.py check
uv run python tool.py test_pages
```
