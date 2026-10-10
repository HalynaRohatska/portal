from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_not_empty(value):
    if not value or value.strip() == "":
        raise ValidationError("Поле не може бути порожнім")

class Thread(models.Model):
    title = models.CharField(max_length=255, validators=[validate_not_empty])
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')

    def __str__(self):
        return self.title

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(validators=[validate_not_empty])
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_messages')

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"

