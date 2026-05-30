from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

from .exam_config import PRODUCT_PHOTO_SIZE


def delete_media_file(file_name):
    if not file_name:
        return

    file_path = Path(settings.MEDIA_ROOT) / file_name
    if file_path.exists() and file_path.is_file():
        file_path.unlink()


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    patronymic = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()


class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class PickupPoint(models.Model):
    address = models.TextField()

    def __str__(self):
        return self.address


class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    article = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)
    description = models.TextField()
    photo = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self):
        return f"{self.article} {self.name}"

    @property
    def final_price(self):
        return self.price * (100 - self.discount) / 100

    def save(self, *args, **kwargs):
        old_photo = ""

        if self.pk:
            old_photo = Product.objects.filter(pk=self.pk).values_list("photo", flat=True).first()

        super().save(*args, **kwargs)

        if old_photo and old_photo != self.photo.name:
            delete_media_file(old_photo)

        self.resize_photo()

    def delete(self, *args, **kwargs):
        photo = self.photo.name
        super().delete(*args, **kwargs)
        delete_media_file(photo)

    def resize_photo(self):
        if not self.photo:
            return

        photo_path = Path(self.photo.path)
        if not photo_path.exists():
            return

        with Image.open(photo_path) as image:
            image.thumbnail(PRODUCT_PHOTO_SIZE)

            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            image.save(photo_path)


class Order(models.Model):
    order_date = models.DateField()
    delivery_date = models.DateField()
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    pickup_code = models.IntegerField()
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)

    def __str__(self):
        return f"Заказ {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.order_id}: {self.product} x {self.count}"
