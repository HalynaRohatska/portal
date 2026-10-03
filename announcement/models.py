from django.db import models
from django.conf import settings
from django.urls import reverse
 
 
class Announcement(models.Model):
    """
    Оголошення групи.
 
    Відповідає п. "Оголошення" ТЗ:
    - відображаються всім користувачам (опубліковані);
    - створювати / редагувати / видаляти можуть лише
      адміністратори та модератори (див. permissions.py).
    """
 
    title = models.CharField("Заголовок", max_length=200)
    content = models.TextField("Текст оголошення")
 
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
        verbose_name="Автор",
    )
 
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Дата оновлення", auto_now=True)
 
    is_pinned = models.BooleanField(
        "Закріпити зверху", default=False,
        help_text="Закріплені оголошення завжди показуються першими.",
    )
    is_published = models.BooleanField(
        "Опубліковано", default=True,
        help_text="Неопубліковані оголошення бачать лише модератори/адміністратори.",
    )
 
    class Meta:
        ordering = ["-is_pinned", "-created_at"]
        verbose_name = "Оголошення"
        verbose_name_plural = "Оголошення"
 
    def __str__(self):
        return self.title
 
    def get_absolute_url(self):
        return reverse("annonc:detail", kwargs={"pk": self.pk})
