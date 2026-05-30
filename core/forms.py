import random

from django import forms
from django.core.exceptions import ValidationError
from PIL import Image

from .exam_config import APP_TEXT
from .models import Order, OrderItem, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "article",
            "photo",
            "name",
            "category",
            "description",
            "manufacturer",
            "supplier",
            "price",
            "unit",
            "quantity",
            "discount",
        ]
        labels = {
            "article": "Артикул",
            "photo": "Фото",
            "name": "Наименование",
            "category": "Категория",
            "description": "Описание",
            "manufacturer": "Производитель",
            "supplier": "Поставщик",
            "price": "Цена",
            "unit": "Единица измерения",
            "quantity": "Количество на складе",
            "discount": "Скидка",
        }

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price < 0:
            raise ValidationError("Цена не может быть отрицательной.")

        return price

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if quantity < 0:
            raise ValidationError("Количество не может быть отрицательным.")

        return quantity

    def clean_discount(self):
        discount = self.cleaned_data["discount"]

        if discount < 0 or discount > 100:
            raise ValidationError("Скидка должна быть от 0 до 100.")

        return discount

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")

        if not photo:
            return photo

        try:
            image = Image.open(photo)
            image.verify()
            photo.seek(0)
        except Exception as error:
            raise ValidationError("Загрузите корректное изображение.") from error

        return photo


class OrderForm(forms.ModelForm):
    products_text = forms.CharField(
        label=APP_TEXT["order_items_label"],
        help_text=APP_TEXT["order_items_help"],
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    class Meta:
        model = Order
        fields = ["products_text", "status", "pickup_point", "order_date", "delivery_date"]
        labels = {
            "status": "Статус заказа",
            "pickup_point": "Пункт выдачи",
            "order_date": "Дата заказа",
            "delivery_date": "Дата выдачи",
        }
        widgets = {
            "order_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "delivery_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            items = []

            for item in self.instance.items.select_related("product"):
                items.append(item.product.article)
                items.append(str(item.count))

            self.fields["products_text"].initial = ", ".join(items)

    def clean_products_text(self):
        value = self.cleaned_data["products_text"]
        parts = [part.strip() for part in value.split(",") if part.strip()]

        if len(parts) % 2 != 0:
            raise ValidationError("После каждого артикула должно быть количество.")

        self.order_items = []

        for index in range(0, len(parts), 2):
            article = parts[index]

            try:
                count = int(parts[index + 1])
            except ValueError as error:
                raise ValidationError("Количество должно быть целым числом.") from error

            if count <= 0:
                raise ValidationError(APP_TEXT["positive_order_count"])

            product = Product.objects.filter(article=article).first()

            if product is None:
                raise ValidationError(f"Товар с артикулом {article} не найден.")

            self.order_items.append((product, count))

        return value

    def save(self, commit=True):
        order = super().save(commit=False)

        if not order.pickup_code:
            order.pickup_code = random.randint(100, 999)

        if commit:
            order.save()
            self.save_items(order)

        return order

    def save_items(self, order):
        OrderItem.objects.filter(order=order).delete()

        for product, count in self.order_items:
            OrderItem.objects.create(order=order, product=product, count=count)
