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

Можно делать вложенные папки, например:

```text
tools/input/task/
tools/input/excel/
tools/input/images/
```

Скрипт читает `input` рекурсивно, поэтому вложенность не мешает.

Картинки тоже можно класть в `tools/input/`, например `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.ico`.
Модель не видит содержимое картинки как человек, но видит имя файла и может попросить скрипт скопировать картинку в проект.

Во время `apply` картинки можно автоматически положить только сюда:

```text
static/images/
media/products/
core/import/
```

Пример: если в `tools/input/images/logo.png` лежит логотип, AI может вернуть команду копирования в JSON, и скрипт положит его в `static/images/logo.png`.

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

Задать один вопрос в консоли:

```powershell
uv run python tool.py ask "почему команда migrate выдает ошибку?"
```

Открыть режим живого диалога:

```powershell
uv run python tool.py chat
```

Выйти из чата:

```text
exit
```

## Как понять, где работает AI

`collect` не обращается к AI. Он только читает файлы и собирает контекст:

```text
[10%] Собираю контекст из input и файлов проекта...
[100%] Контекст собран.
```

`test` обращается к AI один раз и проверяет, что ключ работает.

`plan` обращается к AI один раз и сохраняет текстовый план в `tools/output/plan.md`.

`apply` работает в несколько шагов:

```text
[5%]  собирает контекст
[15%] AI выбирает список файлов для изменения
[25%] разбирает короткий JSON со списком файлов
[30-80%] AI генерирует каждый файл отдельно
[85%] записывает файлы и создает backup
[92%] копирует картинки
[100%] готово
```

Такой режим надежнее, чем просить AI вернуть весь проект одним огромным JSON.

`ask` и `chat` не меняют проект. Они только отправляют вопрос в AI и сохраняют ответ.

Примеры вопросов:

```text
Куда добавить новый маршрут для страницы партнеров?
Почему makemigrations не видит модель?
Как проверить, что import_data заполнил таблицы?
Что значит ошибка TemplateDoesNotExist?
Какой файл открыть, если не работает кнопка удаления?
```

## Результаты

```text
tools/output/context_preview.md
tools/output/plan.md
tools/output/apply_report.md
tools/output/last_response.md
tools/output/apply_manifest_response.md
tools/output/response_core_models.py.md
tools/output/answer_YYYYMMDD_HHMMSS.md
tools/output/chat_log.md
```

Перед заменой файлов скрипт делает backup:

```text
tools/backups/
```

Если `apply` упал с ошибкой, сначала открой:

```text
tools/output/last_response.md
```

Если ошибка произошла до записи файлов, проект не менялся. Если ошибка произошла после записи, восстановление лежит в `tools/backups/`.

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

Картинки скрипт не редактирует, а только копирует из `tools/input/` в разрешенные папки проекта.

Миграции скрипт не создает. Их нужно создать обычной командой Django.
