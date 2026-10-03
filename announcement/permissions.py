from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
 
 
def can_manage_announcements(user) -> bool:
    """
    Повертає True, якщо користувач може створювати / редагувати /
    видаляти оголошення (адміністратор або модератор).
 
    Підлаштуйте цю функцію під реальну реалізацію ролей у проєкті
    (наприклад, під django.contrib.auth.models.Group, якщо ролі
    зберігаються не через поле `role`).
    """
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    return getattr(user, "role", None) in ("moderator", "admin")
 
 
class ModeratorOrAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Дозволяє доступ до в'юшки лише модераторам/адміністраторам."""
 
    def test_func(self):
        return can_manage_announcements(self.request.user)
 
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied(
            "Створювати, редагувати або видаляти оголошення можуть "
            "лише модератори та адміністратори."
        )
 