from django.db import models
import string
import random

def generate_short_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

class ImageEntry(models.Model):
    short_id = models.CharField(max_length=15, default=generate_short_id, unique=True, primary_key=True)
    telegram_file_id = models.CharField(max_length=255)
    telegram_message_id = models.IntegerField(null=True, blank=True)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} ({self.short_id})"

