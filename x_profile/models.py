from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class XrayUser(AbstractUser):
    telegram_user_id = models.CharField(max_length=18)
    current_service = models.ForeignKey('XrayServer', models.SET_NULL, 'server_users', null=True, blank=True)


class XrayServer(models.Model):
    country = models.CharField(max_length=128)
    capacity = models.PositiveIntegerField(default=0)
