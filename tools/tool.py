import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOOL_DIR = Path(__file__).resolve().parent
INPUT_DIR = TOOL_DIR / "input"
OUTPUT_DIR = TOOL_DIR / "output"
BACKUP_DIR = TOOL_DIR / "backups"

TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".py",
    ".html",
    ".css",
    ".csv",
    ".json",
    ".xml",
    ".sql",
}

ASSET_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".ico",
}

PROJECT_FILES = [
    "core/models.py",
    "core/forms.py",
    "core/views.py",
    "core/admin.py",
    "core/permissions.py",
    "core/context_processors.py",
    "core/management/commands/import_data.py",
    "config/settings.py",
    "config/urls.py",
    "static/css/style.css",
    "README.md",
]

PROJECT_FOLDERS = [
    "core/templates/core",
    "docs",
]

ALLOWED_PATHS = PROJECT_FILES + PROJECT_FOLDERS

ALLOWED_ASSET_TARGETS = [
    "static/images",
    "media/products",
    "core/import",
]


def load_local_config():
    path = TOOL_DIR / "local_config.json"
    if not path.exists():
        return {}
    return json.loads(read_text(path))


def ensure_dirs():
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def rel(path):
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


def read_text(path):
    for encoding in ("utf-8", "utf-8-sig", "cp1251"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            pass
    return path.read_text(encoding="utf-8", errors="replace")


def read_xlsx(path):
    from openpyxl import load_workbook

    workbook = load_workbook(path, data_only=True, read_only=True)
    parts = []
    for sheet in workbook.worksheets[:8]:
        parts.append(f"Лист: {sheet.title}")
        for row_number, row in enumerate(sheet.iter_rows(values_only=True), start=1):
            if row_number > 120:
                parts.append("...")
                break
            values = ["" if value is None else str(value) for value in row[:35]]
            parts.append("\t".join(values))
    return "\n".join(parts)


def read_docx(path):
    from docx import Document

    document = Document(path)
    parts = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    for table in document.tables[:10]:
        for row in table.rows[:80]:
            parts.append("\t".join(cell.text.strip() for cell in row.cells))
    return "\n".join(parts)


def read_pdf(path):
    from pypdf import PdfReader

    reader = PdfReader(path)
    parts = []
    for index, page in enumerate(reader.pages[:25], start=1):
        text = page.extract_text() or ""
        if text.strip():
            parts.append(f"Страница {index}\n{text}")
    return "\n\n".join(parts)


def read_known_file(path):
    suffix = path.suffix.lower()
    try:
        if suffix in TEXT_EXTENSIONS:
            return read_text(path)
        if suffix in ASSET_EXTENSIONS:
            return f"Изображение. Имя файла: {path.name}. Размер: {path.stat().st_size} байт. Содержимое картинки не анализируется."
        if suffix in (".xlsx", ".xlsm"):
            return read_xlsx(path)
        if suffix == ".docx":
            return read_docx(path)
        if suffix == ".pdf":
            return read_pdf(path)
    except Exception as error:
        return f"Не удалось прочитать файл: {error}"
    return f"Файл не прочитан как текст. Расширение: {suffix}"


def collect_assignment():
    files = sorted(path for path in INPUT_DIR.rglob("*") if path.is_file())
    if not files:
        return "В папке input пока нет файлов задания."
    parts = []
    for path in files:
        parts.append(f"\n\n===== ФАЙЛ ЗАДАНИЯ: {path.relative_to(INPUT_DIR).as_posix()} =====")
        parts.append(read_known_file(path)[:30000])
    return "\n".join(parts)


def collect_project():
    paths = []
    for name in PROJECT_FILES:
        path = PROJECT_ROOT / name
        if path.exists():
            paths.append(path)
    for folder in PROJECT_FOLDERS:
        base = PROJECT_ROOT / folder
        if base.exists():
            paths.extend(
                path
                for path in base.rglob("*")
                if path.is_file()
                and "__pycache__" not in path.parts
                and path.suffix.lower() in TEXT_EXTENSIONS
            )
    parts = []
    for path in sorted(set(paths)):
        parts.append(f"\n\n===== ФАЙЛ ПРОЕКТА: {rel(path)} =====")
        parts.append(read_known_file(path)[:25000])
    return "\n".join(parts)


def build_context():
    return (
        "# ВЫДАННОЕ ЗАДАНИЕ И ФАЙЛЫ\n"
        f"{collect_assignment()}\n\n"
        "# ТЕКУЩИЕ ФАЙЛЫ ПРОЕКТА\n"
        f"{collect_project()}"
    )


def build_plan_prompt(context):
    return f"""
Ты помогаешь адаптировать простой Django-проект под новое экзаменационное задание.
Сначала внимательно прочитай задание, Excel/PDF/DOCX и текущий код проекта.

Нужно выдать понятный план изменений на русском языке:
1. какие сущности и связи нужны;
2. какие файлы проекта менять;
3. что менять в models.py, forms.py, views.py, urls.py, templates, import_data.py;
4. какие команды потом запустить;
5. какие риски проверить вручную.

Пиши коротко, но конкретно. Код целиком пока не выдавай.

{context}
""".strip()


def build_apply_prompt(context):
    allowed = "\n".join(f"- {path}" for path in ALLOWED_PATHS)
    asset_targets = "\n".join(f"- {path}" for path in ALLOWED_ASSET_TARGETS)
    return f"""
Ты помогаешь адаптировать простой Django-проект под новое экзаменационное задание.
Нужно изменить проект минимально, без сложных абстракций, чтобы он соответствовал заданию и оставался понятным новичку.

Разрешено переписывать только эти файлы и папки:
{allowed}

Картинки из tools/input можно копировать только в эти папки:
{asset_targets}

Не создавай миграции. Пользователь сам выполнит makemigrations и migrate.
Не добавляй комментарии в код без необходимости.
Не меняй секреты, пароли и API-ключи.
Не используй сложные универсальные конфиги.
Сохраняй стиль простого Django-кода: models, forms, views, templates, management command.

Ответ верни строго в JSON без Markdown:
{{
  "summary": "кратко что изменено",
  "steps": ["что потом проверить"],
  "commands": ["команды после применения"],
  "files": [
    {{
      "path": "core/models.py",
      "content": "полный новый текст файла"
    }}
  ],
  "assets": [
    {{
      "source": "images/logo.png",
      "target": "static/images/logo.png"
    }}
  ]
}}

В files включай только те файлы, которые реально надо заменить. Каждый content должен быть полным содержимым файла.
В assets включай только картинки, которые нужно скопировать из tools/input в проект. source - путь относительно tools/input. target - путь относительно корня Django-проекта.
Если картинки не нужны, верни пустой список assets.

{context}
""".strip()


def call_yandex(prompt):
    from yandex_ai_studio_sdk import AIStudio

    local_config = load_local_config()
    api_key = local_config.get("YC_API_KEY")
    folder_id = local_config.get("YC_FOLDER_ID")
    model_name = local_config.get("YC_MODEL", "yandexgpt")
    model_version = local_config.get("YC_MODEL_VERSION", "rc")
    temperature = float(local_config.get("YC_TEMPERATURE", "0.2"))

    if not api_key or not folder_id:
        raise RuntimeError("Заполни YC_API_KEY и YC_FOLDER_ID в tools/local_config.json")
    if "/folders/" in folder_id:
        folder_id = folder_id.rstrip("/").split("/folders/", 1)[1].split("?", 1)[0]

    sdk = AIStudio(folder_id=folder_id, auth=api_key)
    try:
        model = sdk.models.completions(model_name, model_version=model_version)
    except TypeError:
        model = sdk.models.completions(model_name)
    model = model.configure(temperature=temperature)
    result = model.run(prompt)
    return result[0].text


def extract_json(text):
    cleaned = text.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL)
    if fenced:
        cleaned = fenced.group(1).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Модель не вернула JSON с объектом.")
    return json.loads(cleaned[start : end + 1])


def is_allowed(relative_path):
    normalized = Path(relative_path).as_posix().lstrip("/")
    if ".." in Path(normalized).parts:
        return False
    for allowed in ALLOWED_PATHS:
        allowed = Path(allowed).as_posix().rstrip("/")
        if normalized == allowed or normalized.startswith(f"{allowed}/"):
            return True
    return False


def is_asset_target_allowed(relative_path):
    normalized = Path(relative_path).as_posix().lstrip("/")
    if ".." in Path(normalized).parts:
        return False
    for allowed in ALLOWED_ASSET_TARGETS:
        allowed = Path(allowed).as_posix().rstrip("/")
        if normalized.startswith(f"{allowed}/"):
            return True
    return False


def write_files(data):
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = BACKUP_DIR / timestamp
    changed = []
    for item in data.get("files", []):
        path_name = item.get("path", "")
        content = item.get("content")
        if not path_name or content is None:
            continue
        if not is_allowed(path_name):
            raise ValueError(f"Запрещенный путь для записи: {path_name}")
        target = (PROJECT_ROOT / path_name).resolve()
        if PROJECT_ROOT.resolve() not in target.parents and target != PROJECT_ROOT.resolve():
            raise ValueError(f"Путь вышел за пределы проекта: {path_name}")
        if target.exists():
            backup = backup_root / path_name
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        changed.append(path_name)
    return changed, backup_root


def validate_assets(data):
    assets = []
    for item in data.get("assets", []):
        source_name = item.get("source", "")
        target_name = item.get("target", "")
        if not source_name or not target_name:
            continue
        source = (INPUT_DIR / source_name).resolve()
        target = (PROJECT_ROOT / target_name).resolve()
        if INPUT_DIR.resolve() not in source.parents:
            raise ValueError(f"Путь картинки вышел за пределы input: {source_name}")
        if PROJECT_ROOT.resolve() not in target.parents:
            raise ValueError(f"Путь картинки вышел за пределы проекта: {target_name}")
        if not source.exists():
            raise ValueError(f"Картинка не найдена в input: {source_name}")
        if source.suffix.lower() not in ASSET_EXTENSIONS:
            raise ValueError(f"Файл не является разрешенной картинкой: {source_name}")
        if not is_asset_target_allowed(target_name):
            raise ValueError(f"Запрещенный путь для картинки: {target_name}")
        assets.append((source, target, target_name))
    return assets


def copy_assets(assets, backup_root):
    copied = []
    for source, target, target_name in assets:
        if target.exists():
            backup = backup_root / target_name
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target_name)
    return copied


def save_output(name, content):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / name
    path.write_text(content, encoding="utf-8")
    return path


def command_collect():
    context = build_context()
    path = save_output("context_preview.md", context)
    print(f"Контекст собран: {path}")


def command_plan():
    context = build_context()
    prompt = build_plan_prompt(context)
    answer = call_yandex(prompt)
    save_output("last_response.md", answer)
    path = save_output("plan.md", answer)
    print(f"План сохранен: {path}")


def command_apply():
    context = build_context()
    prompt = build_apply_prompt(context)
    answer = call_yandex(prompt)
    save_output("last_response.md", answer)
    data = extract_json(answer)
    assets = validate_assets(data)
    changed, backup = write_files(data)
    copied_assets = copy_assets(assets, backup)
    report = [
        f"# Отчет AI-помощника {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        data.get("summary", ""),
        "",
        "## Измененные файлы",
        *(f"- {path}" for path in changed),
        "",
        "## Скопированные картинки",
        *(f"- {path}" for path in copied_assets),
        "",
        "## Backup",
        str(backup),
        "",
        "## Команды",
        *(f"```powershell\n{command}\n```" for command in data.get("commands", [])),
        "",
        "## Проверить",
        *(f"- {step}" for step in data.get("steps", [])),
    ]
    path = save_output("apply_report.md", "\n".join(report))
    print(f"Изменено файлов: {len(changed)}")
    print(f"Скопировано картинок: {len(copied_assets)}")
    print(f"Отчет: {path}")
    print(f"Backup: {backup}")


def command_test():
    answer = call_yandex("Ответь одним предложением: API Yandex AI Studio работает.")
    print(answer.strip())


def main():
    ensure_dirs()
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["collect", "test", "plan", "apply"])
    args = parser.parse_args()

    commands = {
        "collect": command_collect,
        "test": command_test,
        "plan": command_plan,
        "apply": command_apply,
    }
    try:
        commands[args.command]()
    except Exception as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
