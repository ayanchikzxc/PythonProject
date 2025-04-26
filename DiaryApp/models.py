from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings
from cloudinary.models import CloudinaryField

fernet = Fernet(settings.FERNET_KEY)

class DiaryEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('neutral', 'Neutral'),
        ('angry', 'Angry'),
        ('excited', 'Excited'),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    image = CloudinaryField('image', blank=True, null=True)  # подключение картинок

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            fernet.decrypt(self.content.encode())
        except:
            self.content = fernet.encrypt(self.content.encode()).decode()
        super().save(*args, **kwargs)

    def get_decrypted_content(self):
        try:
            return fernet.decrypt(self.content.encode()).decode()
        except Exception:
            return ""
