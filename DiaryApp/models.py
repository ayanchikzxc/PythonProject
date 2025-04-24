from django.db import models
from django.contrib.auth.models import User

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries", null=True)

    def __str__(self):
        return self.title
