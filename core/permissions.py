from .exam_config import ADMIN_ROLES, MANAGER_ROLES


def user_role(user):
    role = getattr(user, "role", None)
    return getattr(role, "name", "")


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user_role(user) in ADMIN_ROLES)


def is_manager_or_admin(user):
    allowed_roles = ADMIN_ROLES + MANAGER_ROLES
    return user.is_authenticated and (user.is_superuser or user_role(user) in allowed_roles)
