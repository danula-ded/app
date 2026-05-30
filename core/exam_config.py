APP_TEXT = {
    "company_name": "ООО Обувь",
    "catalog_menu": "Товары",
    "orders_menu": "Заказы",
    "catalog_title": "Список товаров",
    "add_item": "Добавить товар",
    "edit_item": "Редактирование товара",
    "delete_item": "Удаление товара",
    "item_id": "ID товара",
    "item_empty": "Товары не найдены.",
    "delete_item_question": "Удалить товар",
    "delete_item_warning": "Если товар есть в заказе, удаление будет запрещено.",
    "item_added": "Товар добавлен.",
    "item_updated": "Товар обновлен.",
    "item_deleted": "Товар удален.",
    "item_delete_blocked": "Товар нельзя удалить, потому что он есть в заказе.",
    "search_placeholder": "Поиск",
    "all_suppliers": "Все поставщики",
    "sort_default": "По порядку",
    "sort_quantity_asc": "Количество по возрастанию",
    "sort_quantity_desc": "Количество по убыванию",
    "orders_title": "Заказы",
    "add_order": "Добавить заказ",
    "edit_order": "Редактирование заказа",
    "delete_order": "Удаление заказа",
    "order_id": "ID заказа",
    "order_items_header": "Товары",
    "order_date": "Дата заказа",
    "order_delivery_date": "Дата выдачи",
    "order_empty": "Заказы не найдены.",
    "delete_order_question": "Удалить заказ",
    "order_added": "Заказ добавлен.",
    "order_updated": "Заказ обновлен.",
    "order_deleted": "Заказ удален.",
    "orders_forbidden": "Раздел заказов доступен менеджеру и администратору.",
    "admin_only": "Это действие доступно только администратору.",
    "order_items_label": "Артикулы товаров",
    "order_items_help": "Формат: А112Т4, 2, F635R4, 2",
    "positive_order_count": "Количество товара в заказе должно быть больше нуля.",
}

ADMIN_ROLES = ("admin", "Администратор")
MANAGER_ROLES = ("manager", "Менеджер")
CLIENT_ROLES = ("client", "Авторизированный клиент")

PRODUCT_RELATIONS = ("category", "manufacturer", "supplier", "unit")

PRODUCT_SEARCH_FIELDS = (
    "article",
    "name",
    "description",
    "category__name",
    "manufacturer__name",
    "supplier__name",
    "unit__name",
)

PRODUCT_SORTS = {
    "quantity_asc": ("quantity", "id"),
    "quantity_desc": ("-quantity", "id"),
}

PRODUCT_PHOTO_SIZE = (300, 200)
