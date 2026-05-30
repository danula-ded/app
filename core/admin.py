from django.contrib import admin

from .models import (
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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "order_date", "delivery_date", "pickup_point", "status")


admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(OrderStatus)
admin.site.register(PickupPoint)
admin.site.register(Product)
admin.site.register(Role)
admin.site.register(Supplier)
admin.site.register(Unit)
admin.site.register(User)
