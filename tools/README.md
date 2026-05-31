# Инструмент адаптации проекта

Это отдельный мини-проект. Он лежит в папке `tools` и не добавляет зависимости в основной Django-проект.

## Куда вставлять токен

Токен вставляется только сюда:

```text
tools/local_config.json
```

Открыть файл:

```powershell
cd tools
notepad local_config.json
```

Заполни:

```json
{
  "YC_API_KEY": "твой_api_ключ",
  "YC_FOLDER_ID": "твой_folder_id",
  "YC_MODEL": "yandexgpt",
  "YC_MODEL_VERSION": "rc",
  "YC_TEMPERATURE": "0.2"
}
```

В git лежит этот же файл с пустым шаблоном. Настоящий API-ключ лучше вставлять локально перед запуском.

## Что такое Folder ID

`YC_FOLDER_ID` - это идентификатор каталога в Yandex Cloud.

Проще всего взять его из ссылки:

```text
https://console.yandex.cloud/folders/<folder_id>
```

Можно вставить и сам ID, и полную ссылку на каталог.

## Установка

Из корня Django-проекта:

```powershell
cd tools
uv sync
```

## Куда класть задание

Все файлы задания клади сюда:

```text
tools/input/
```

Поддерживаются `.txt`, `.md`, `.pdf`, `.docx`, `.xlsx`, `.csv`.

## Команды

Проверить чтение файлов без обращения к AI:

```powershell
uv run python tool.py collect
```

Проверить API-ключ:

```powershell
uv run python tool.py test
```

Получить план без изменения проекта:

```powershell
uv run python tool.py plan
```

Применить изменения к разрешенным файлам проекта:

```powershell
uv run python tool.py apply
```

## Результаты

```text
tools/output/context_preview.md
tools/output/plan.md
tools/output/apply_report.md
tools/output/last_response.md
```

Перед заменой файлов скрипт делает backup:

```text
tools/backups/
```

После `apply`:

```powershell
cd ..
uv run python manage.py check
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py import_data
uv run python manage.py runserver
```

## Что скрипт умеет менять

```text
core/models.py
core/forms.py
core/views.py
core/admin.py
core/permissions.py
core/context_processors.py
core/management/commands/import_data.py
config/settings.py
config/urls.py
core/templates/core/
static/css/style.css
docs/
README.md
```

Миграции скрипт не создает. Их нужно создать обычной командой Django.
