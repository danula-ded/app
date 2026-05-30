def user_role(user):
    role = getattr(user, "role", None)
    return getattr(role, "name", "")


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user_role(user) in ("admin", "Администратор"))


def is_manager_or_admin(user):
    allowed_roles = ("admin", "Администратор", "manager", "Менеджер")
    return user.is_authenticated and (user.is_superuser or user_role(user) in allowed_roles)
