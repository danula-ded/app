# ER-диаграмма

Файл:

```text
docs/er_diagram.pdf
```

Диаграмма содержит основные таблицы проекта:

- `Role`;
- `User`;
- `Supplier`;
- `Manufacturer`;
- `Category`;
- `Unit`;
- `Product`;
- `PickupPoint`;
- `OrderStatus`;
- `Order`;
- `OrderItem`.

Основные связи:

- `User.role_id -> Role.id`;
- `Product.category_id -> Category.id`;
- `Product.manufacturer_id -> Manufacturer.id`;
- `Product.supplier_id -> Supplier.id`;
- `Product.unit_id -> Unit.id`;
- `Order.pickup_point_id -> PickupPoint.id`;
- `Order.status_id -> OrderStatus.id`;
- `Order.user_id -> User.id`;
- `OrderItem.order_id -> Order.id`;
- `OrderItem.product_id -> Product.id`.
