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
  "YC_API_MODE": "sdk",
  "YC_MODEL": "yandexgpt",
  "YC_MODEL_VERSION": "rc",
  "YC_TEMPERATURE": "0.2"
}
```

В git лежит этот же файл с пустым шаблоном. Настоящий API-ключ лучше вставлять локально перед запуском.

Для Qwen через OpenAI-compatible API можно поставить:

```json
{
  "YC_API_KEY": "твой_api_ключ",
  "YC_FOLDER_ID": "твой_folder_id",
  "YC_API_MODE": "openai",
  "YC_MODEL": "qwen3-235b-a22b-fp8",
  "YC_MODEL_VERSION": "latest",
  "YC_TEMPERATURE": "0.1"
}
```

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

Excel/CSV для импорта можно оставлять в `tools/input` или во вложенной папке вроде `tools/input/Ресурсы`. Во время `apply` скрипт сам скопирует все `.xlsx`, `.xlsm` и `.csv` в проект:

```text
core/import/
```

Поэтому `import_data.py` должен читать файлы из `core/import`, а не из `tools/input` и не из папки `Ресурсы`.

Картинки тоже можно класть в `tools/input/`, например `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.ico`.
Модель не видит содержимое картинки как человек, но видит имя файла и может попросить скрипт скопировать картинку в проект.

Во время `apply` картинки можно автоматически положить только сюда:

```text
static/images/
media/products/
core/import/
```

Если AI случайно укажет `static/icons/` или `static/img/`, скрипт автоматически переложит такой путь в `static/images/`.

Пример: если в `tools/input/images/logo.png` лежит логотип, AI может вернуть команду копирования в JSON, и скрипт положит его в `static/images/logo.png`.

Если картинка лежит во вложенной папке, можно указывать полный путь от `tools/input`:

```text
Ресурсы/Мастер пол.ico
```

Если указан только файл:

```text
Мастер пол.ico
```

скрипт сам попробует найти его во всех подпапках `tools/input`. Если файлов с таким именем несколько, он остановится и покажет варианты, чтобы случайно не взять неправильную картинку.

## Команды

Проверить чтение файлов без обращения к AI:

```powershell
uv run python tool.py collect
```

`collect` делает `tools/output/context_preview.md`. В начале файла отдельным блоком выводятся Excel-таблицы: имя файла, лист, размер, заголовки колонок и примеры строк. Именно по этому блоку модель понимает, какие сущности и поля нужны в `models.py`.

В проектный контекст специально не добавляются `docs/*.md` и `README.md`, чтобы старые гайды не путали модель при смене предметной области. Для генерации остаются код, шаблоны и CSS.

Во время `apply` скрипт не создает и не переписывает `README.md`, `docs/*.md` и любые другие Markdown-файлы проекта. Markdown остается только для служебных отчетов внутри `tools/output/`.

Проверить API-ключ:

```powershell
uv run python tool.py test
```

Получить план без изменения проекта:

```powershell
uv run python tool.py plan
```

Сгенерировать только модели, admin.py и импорт:

```powershell
uv run python tool.py schema
```

После `schema` обычно запускают:

```powershell
cd ..
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py import_data
cd tools
```

Сгенерировать интерфейс после готовой схемы:

```powershell
uv run python tool.py interface
```

Проверить соответствие проекта заданию без изменения файлов:

```powershell
uv run python tool.py audit
```

Можно проверить конкретное условие:

```powershell
uv run python tool.py audit "проверь, есть ли поиск, фильтрация, сортировка и CRUD"
```

Старый режим "сделать все сразу":

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

Восстановить файлы из последнего backup:

```powershell
uv run python tool.py restore
```

Восстановить конкретный backup:

```powershell
uv run python tool.py restore 20260531_145542
```

Проверить проект так же, как это делает `apply`:

```powershell
uv run python tool.py check
```

Эта команда проверяет синтаксис основных Python-файлов, компиляцию шаблонов и запускает:

```powershell
uv run python manage.py check
```

Проверить страницы после миграций и импорта данных:

```powershell
uv run python tool.py test_pages
```

Эту команду запускай только после `makemigrations`, `migrate` и `import_data`, потому что страницы часто обращаются к таблицам базы данных.

Попробовать автоматически исправить ошибку после проверки:

```powershell
uv run python tool.py repair
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

`schema` обращается к AI и меняет только:

```text
core/models.py
core/admin.py
core/management/commands/import_data.py
```

Он не трогает `settings.py`, `views.py`, `forms.py`, `urls.py` и шаблоны. Excel/CSV копируются в `core/import`.

`interface` обращается к AI и меняет только интерфейсные файлы:

```text
core/forms.py
core/views.py
config/urls.py
core/templates/core/
static/css/style.css
core/permissions.py
core/context_processors.py
```

Он берет текущий `core/models.py` как источник правды и не трогает `config/settings.py`.

`audit` обращается к AI, но не меняет проект. Он проверяет соответствие кода заданию и пишет, чего не хватает.

`apply` работает в несколько шагов:

```text
[5%]  собирает контекст
[10%] AI строит единый blueprint проекта по заданию и Excel
[15%] AI выбирает список файлов для изменения
[25%] разбирает короткий JSON со списком файлов
[25%] если AI указал папку вместо файла, уточняет конкретные файлы
[30-80%] AI генерирует каждый файл отдельно в порядке models -> forms -> views -> urls -> templates -> import_data
[30-80%] каждый следующий файл получает уже сгенерированные файлы в контексте
[30-80%] если файл пришел без нужного формата, повторяет запрос
[82%] проверяет согласованность urls/views/templates/forms/models/import_data до записи
[85%] записывает файлы и создает backup
[92%] копирует картинки
[92%] копирует Excel/CSV из tools/input в core/import
[93%] запускает py_compile, manage.py check и компиляцию шаблонов
[94%] если проверка упала, пытается исправить проект
[100%] готово
```

Такой режим надежнее, чем просить AI вернуть весь проект одним огромным JSON.

Внутренняя проверка до записи ловит типовые ошибки:

```text
config/urls.py импортирует view, которого нет в core/views.py
views/forms/admin/import_data импортируют модель или форму, которой нет
core/views.py ссылается на шаблон, которого нет
config/urls.py потерял admin/ или главную страницу
HTML-шаблон использует url name, которого нет в config/urls.py
HTML-шаблон расширяет base.html вместо core/base.html
HTML-шаблон использует static без load static
HTML-шаблон содержит POST-форму без csrf_token
HTML-шаблон содержит markdown-строки ```html
list-страница потеряла поиск, фильтр или сортировку
forms.py использует поле, которого нет в models.py
import_data.py пишет поле, которого нет в models.py
import_data.py читает Excel/CSV из неправильной папки
import_data.py вызывает get_or_create без обязательных полей
```

`config/settings.py` теперь считается ручной настройкой. Инструмент читает его как контекст, но не переписывает. Базу данных, `AUTH_USER_MODEL`, `LOGIN_REDIRECT_URL` и другие базовые настройки лучше поправлять руками.

Blueprint сохраняется здесь:

```text
tools/output/blueprint.md
```

Это короткая "память" текущей генерации: сущности, Excel-файлы, страницы, формы, assets. Следующие запросы получают этот blueprint и уже сгенерированные файлы, поэтому инструмент меньше похож на набор отдельных чатов.

Если модель вместо blueprint вернула отказ или обычный текст, скрипт повторит запрос. Если повтор тоже не даст JSON, будет создан запасной blueprint по Excel-таблицам, чтобы генерация не шла с пустой архитектурой.

`ask` и `chat` не меняют проект. Они только отправляют вопрос в AI и сохраняют ответ.
Если в вопросе написано имя файла, например `consistency_errors_final.md`, `config/urls.py` или `response_core_admin.py.md`, скрипт пытается найти этот файл в проекте или в `tools/output/`, читает его и прикладывает к вопросу.

`restore` не обращается к AI. Он возвращает файлы проекта из `tools/backups`.

`check` не обращается к AI. Он запускает проверку Django без открытия страниц и сохраняет вывод.

`test_pages` запускается после миграций и импорта данных. Он проверяет проект, открывает доступные страницы через Django test client и, если проверка упала, пытается исправить код через AI.
Если таблицы базы еще не созданы, `test_pages` не запускает исправление, а просит сначала выполнить миграции и импорт.

`repair` обращается к AI только если проверка Django упала. Он передает ошибку, просит исправить минимальный набор файлов и снова запускает проверку.

`apply`, `repair` и исправление согласованности делают до 5 попыток. При каждой новой попытке AI получает текущие уже сгенерированные или записанные файлы и текст последней ошибки.

Проверка страниц вынесена из `apply`, чтобы сначала можно было спокойно создать миграции, применить их и наполнить базу.

Примеры вопросов:

```text
Куда добавить новый маршрут для страницы партнеров?
Почему makemigrations не видит модель?
Как проверить, что import_data заполнил таблицы?
Что значит ошибка TemplateDoesNotExist?
Какой файл открыть, если не работает кнопка удаления?
Почему apply упал и что написано в consistency_errors_final.md?
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

Быстро восстановить последний backup:

```powershell
uv run python tool.py restore
```

Если ошибка похожа на:

```text
Permission denied: core/templates/core
```

значит AI указал папку вместо конкретного HTML-файла. В новой версии скрипт старается автоматически уточнить список файлов. Если ошибка всё равно повторилась, открой `tools/output/apply_manifest_response.md` и замени путь папки на конкретные шаблоны, например:

```text
core/templates/core/partner_list.html
core/templates/core/partner_form.html
```

Если ошибка связана с картинкой, проверь:

```powershell
Get-ChildItem -Recurse tools/input
```

В сообщении об ошибке скрипт покажет доступные картинки или попросит указать точный путь от `tools/input`.

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
```

Картинки скрипт не редактирует, а только копирует из `tools/input/` в разрешенные папки проекта.

Миграции скрипт не создает. Их нужно создать обычной командой Django.

uv run python tool.py ask "почему не работает импорт?"
uv run python tool.py chat

uv run python tool.py collect
uv run python tool.py test
uv run python tool.py plan
uv run python tool.py schema
uv run python tool.py interface
uv run python tool.py audit
uv run python tool.py apply
uv run python tool.py test_pages

----

После `apply`:

```powershell
cd ..
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py import_data
cd tools
uv run python tool.py test_pages
cd ..
uv run python manage.py runserver
```

## Ручной режим после сбоя apply

Если `apply` не смог полностью собрать проект, дальше можно работать через `ask` или `chat`.

`ask` задает один вопрос и сразу завершает работу:

```powershell
cd tools
uv run python tool.py ask "Посмотри consistency_errors_final.md и объясни, какие файлы не согласованы"
```

`chat` открывает диалог. Его удобно держать открытым и задавать вопросы по очереди:

```powershell
cd tools
uv run python tool.py chat
```

Выйти из чата:

```text
exit
```

Как передавать файлы в вопросе:

```text
core/admin.py
core/models.py
config/urls.py
tools/output/consistency_errors_final.md
response_core_admin.py.md
```

Абсолютный путь тоже можно указать, лучше в кавычках или обратных кавычках, потому что в пути могут быть пробелы:

```powershell
uv run python tool.py ask "Прочитай `C:\Users\Даниил\Desktop\test demo\app\core\admin.py` и объясни, что в нем исправить"
```

Если нужен полный файл с кодом, проси прямо так:

```powershell
uv run python tool.py ask "Прочитай core/models.py и core/admin.py. Верни полный новый текст файла core/admin.py без markdown и без пояснений"
```

Или так:

```powershell
uv run python tool.py ask "Посмотри core/views.py, config/urls.py и core/templates/core/partner_list.html. Скажи, почему страница не открывается, и дай минимальные правки"
```

Что AI видит в `ask` и `chat`:

```text
tools/input/                 файлы задания, Excel, PDF, DOCX, картинки по именам
основные файлы проекта       models.py, forms.py, views.py, urls.py, templates, css
tools/output/                последние отчеты apply/check/consistency
файлы из вопроса             если ты явно написал имя файла или путь
```

AI не читает диск сам по своему желанию. Сначала скрипт собирает текст нужных файлов, потом отправляет его в модель. Поэтому если хочешь, чтобы AI точно учел конкретный файл, напиши его имя в вопросе.

`ask` и `chat` не записывают изменения в проект. Они дают совет или полный текст файла. Для автоматической записи используй:

```powershell
uv run python tool.py apply
uv run python tool.py repair
```
