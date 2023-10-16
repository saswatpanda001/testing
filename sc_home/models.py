from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()
# Create your models here.
class feedback_model(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="feedback_writer")
    created = models.DateTimeField(default=timezone.now)
    feed = models.TextField(blank=True, null=True)
    topic = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.topic)