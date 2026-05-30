from calendar import monthrange
from datetime import date, datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from openpyxl import load_workbook

from core.models import (
    Category,
    Manufacturer,
    Order,
    OrderItem,
    OrderStatus,
    PickupPoint,
    Product,
    Role,
    Supplier,
    Unit,
    User,
)


FILES = {
    "points": "Пункты выдачи_import.xlsx",
    "products": "Tovar.xlsx",
    "users": "user_import.xlsx",
    "orders": "Заказ_import.xlsx",
}

PRODUCT = {
    "article": 0,
    "name": 1,
    "unit": 2,
    "price": 3,
    "supplier": 4,
    "manufacturer": 5,
    "category": 6,
    "discount": 7,
    "quantity": 8,
    "description": 9,
    "photo": 10,
}

USER = {
    "role": 0,
    "full_name": 1,
    "login": 2,
    "password": 3,
}

ORDER = {
    "id": 0,
    "items": 1,
    "order_date": 2,
    "delivery_date": 3,
    "pickup_point": 4,
    "user": 5,
    "pickup_code": 6,
    "status": 7,
}

ROLE_MAP = {
    "Администратор": "admin",
    "Менеджер": "manager",
    "Авторизированный клиент": "client",
}

DATE_FORMATS = ("%d.%m.%Y", "%Y-%m-%d")


def cell(row, column):
    if column >= len(row):
        return None

    return row[column]


def text(value):
    if value is None:
        return ""

    return str(value).replace("\xa0", " ").strip()


def number(value, default=0):
    if value in (None, ""):
        return default

    return value


def excel_date(value):
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    value_text = text(value)

    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value_text, date_format).date()
        except ValueError:
            pass

    parts = value_text.split(".")

    if len(parts) == 3 and all(part.isdigit() for part in parts):
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])

        if 1 <= month <= 12:
            last_day = monthrange(year, month)[1]
            return date(year, month, min(day, last_day))

    return None


def split_name(full_name):
    parts = text(full_name).split()
    last_name = parts[0] if len(parts) > 0 else ""
    first_name = parts[1] if len(parts) > 1 else ""
    patronymic = " ".join(parts[2:]) if len(parts) > 2 else ""
    return last_name, first_name, patronymic


class Command(BaseCommand):
    def handle(self, *args, **options):
        folder = settings.BASE_DIR / "import"
        if not folder.exists():
            folder = settings.BASE_DIR / "core" / "import"

        self.run_if_exists(folder, "points", self.import_pickup_points)
        self.run_if_exists(folder, "products", self.import_products)
        self.run_if_exists(folder, "users", self.import_users)
        self.run_if_exists(folder, "orders", self.import_orders)

        self.stdout.write(self.style.SUCCESS("Импорт завершен"))
        self.stdout.write(f"Товаров: {Product.objects.count()}")
        self.stdout.write(f"Заказов: {Order.objects.count()}")
        self.stdout.write(f"Позиций заказов: {OrderItem.objects.count()}")

    def run_if_exists(self, folder, file_key, import_function):
        filename = FILES[file_key]

        if not (folder / filename).exists():
            self.stdout.write(f"Файл {filename} не найден, импорт пропущен")
            return

        import_function(folder)

    def rows(self, folder, file_key, start=2):
        sheet = load_workbook(folder / FILES[file_key], data_only=True).active
        return sheet.iter_rows(min_row=start, values_only=True)

    def import_pickup_points(self, folder):
        for row in self.rows(folder, "points", start=1):
            address = text(cell(row, 0))

            if address:
                PickupPoint.objects.get_or_create(address=address)

    def import_products(self, folder):
        for row in self.rows(folder, "products"):
            article = text(cell(row, PRODUCT["article"]))

            if not article:
                continue

            supplier, _ = Supplier.objects.get_or_create(name=text(cell(row, PRODUCT["supplier"])))
            manufacturer, _ = Manufacturer.objects.get_or_create(name=text(cell(row, PRODUCT["manufacturer"])))
            category, _ = Category.objects.get_or_create(name=text(cell(row, PRODUCT["category"])))
            unit, _ = Unit.objects.get_or_create(name=text(cell(row, PRODUCT["unit"])) or "шт.")
            photo = text(cell(row, PRODUCT["photo"]))

            Product.objects.update_or_create(
                article=article,
                defaults={
                    "name": text(cell(row, PRODUCT["name"])),
                    "unit": unit,
                    "price": number(cell(row, PRODUCT["price"])),
                    "supplier": supplier,
                    "manufacturer": manufacturer,
                    "category": category,
                    "discount": number(cell(row, PRODUCT["discount"])),
                    "quantity": number(cell(row, PRODUCT["quantity"])),
                    "description": text(cell(row, PRODUCT["description"])),
                    "photo": f"products/{photo}" if photo else "",
                },
            )

    def import_users(self, folder):
        for row in self.rows(folder, "users"):
            role_from_excel = text(cell(row, USER["role"]))
            last_name, first_name, patronymic = split_name(cell(row, USER["full_name"]))
            login = text(cell(row, USER["login"]))
            password = text(cell(row, USER["password"]))

            if not login:
                continue

            role_name = ROLE_MAP.get(role_from_excel, role_from_excel)
            role, _ = Role.objects.get_or_create(name=role_name)

            user, _ = User.objects.update_or_create(
                username=login,
                defaults={
                    "email": login,
                    "last_name": last_name,
                    "first_name": first_name,
                    "patronymic": patronymic,
                    "role": role,
                },
            )
            user.set_password(password)
            user.save()

    def import_orders(self, folder):
        for row in self.rows(folder, "orders"):
            order_id = cell(row, ORDER["id"])
            order_date = excel_date(cell(row, ORDER["order_date"]))
            delivery_date = excel_date(cell(row, ORDER["delivery_date"]))

            if not order_id:
                continue

            if not order_date or not delivery_date:
                self.stdout.write(f"Заказ {order_id} пропущен: неправильная дата")
                continue

            pickup_point = PickupPoint.objects.filter(id=cell(row, ORDER["pickup_point"])).first()
            if pickup_point is None:
                pickup_point = PickupPoint.objects.first()

            status, _ = OrderStatus.objects.get_or_create(name=text(cell(row, ORDER["status"])))

            order, _ = Order.objects.update_or_create(
                id=order_id,
                defaults={
                    "order_date": order_date,
                    "delivery_date": delivery_date,
                    "pickup_point": pickup_point,
                    "user": self.find_user(cell(row, ORDER["user"])),
                    "pickup_code": number(cell(row, ORDER["pickup_code"])),
                    "status": status,
                },
            )

            OrderItem.objects.filter(order=order).delete()
            self.create_order_items(order, text(cell(row, ORDER["items"])))

    def create_order_items(self, order, items_text):
        parts = [part.strip() for part in items_text.split(",") if part.strip()]

        for index in range(0, len(parts), 2):
            if index + 1 >= len(parts):
                continue

            product = Product.objects.filter(article=parts[index]).first()

            if product:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    count=int(parts[index + 1]),
                )

    def find_user(self, full_name):
        last_name, first_name, patronymic = split_name(full_name)
        return User.objects.filter(
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
        ).first()
