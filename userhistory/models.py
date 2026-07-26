from django.conf import settings
from django.db import models


class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    path = models.CharField(max_length=255)
    page_name = models.CharField(max_length=120)
    method = models.CharField(max_length=10, default='GET')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'user activities'

    def __str__(self):
        return f'{self.user.username} visited {self.page_name}'
