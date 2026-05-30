from .exam_config import APP_TEXT
from .permissions import is_manager_or_admin


def menu_permissions(request):
    return {
        "app_text": APP_TEXT,
        "can_open_orders_menu": is_manager_or_admin(request.user),
    }
