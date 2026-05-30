from .permissions import is_manager_or_admin


def menu_permissions(request):
    return {
        "can_open_orders_menu": is_manager_or_admin(request.user),
    }
