from django.db import models


class Message(models.Model):
    text = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
