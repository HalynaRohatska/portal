from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Announcement

User = get_user_model()


class AnnouncementPermissionsTests(TestCase):
    """Перевірка, що доступ до CRUD оголошень відповідає ролям із ТЗ."""

    def setUp(self):
        self.regular_user = User.objects.create_user(
            username="student", password="pass12345"
        )
        # Якщо у вашій моделі User немає поля role — приберіть цей рядок,
        # а модератора призначайте через ваш реальний механізм ролей.
        self.moderator = User.objects.create_user(
            username="moderator", password="pass12345"
        )
        if hasattr(self.moderator, "role"):
            self.moderator.role = "moderator"
            self.moderator.save()

        self.admin = User.objects.create_superuser(
            username="admin", password="pass12345", email="admin@example.com"
        )

        self.announcement = Announcement.objects.create(
            title="Тестове оголошення",
            content="Це текст тестового оголошення для перевірки CRUD.",
            created_by=self.admin,
        )

    def test_list_page_available_to_everyone(self):
        response = self.client.get(reverse("announcements:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестове оголошення")

    def test_unpublished_hidden_from_regular_user(self):
        self.announcement.is_published = False
        self.announcement.save()

        self.client.login(username="student", password="pass12345")
        response = self.client.get(reverse("announcements:list"))
        self.assertNotContains(response, "Тестове оголошення")

    def test_regular_user_cannot_create(self):
        self.client.login(username="student", password="pass12345")
        response = self.client.post(reverse("announcements:create"), {
            "title": "Нове оголошення",
            "content": "Спроба створення від звичайного користувача.",
        })
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create(self):
        self.client.login(username="admin", password="pass12345")
        response = self.client.post(reverse("announcements:create"), {
            "title": "Оголошення від адміністратора",
            "content": "Текст оголошення довжиною понад 10 символів.",
            "is_published": "on",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Announcement.objects.filter(title="Оголошення від адміністратора").exists()
        )

    def test_short_title_is_invalid(self):
        self.client.login(username="admin", password="pass12345")
        response = self.client.post(reverse("announcements:create"), {
            "title": "ОК",
            "content": "Текст оголошення довжиною понад 10 символів.",
        })
        self.assertEqual(response.status_code, 200)  # форма з помилкою
        self.assertFalse(Announcement.objects.filter(title="ОК").exists())