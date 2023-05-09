from django.db import models

# Create your models here.
class XrayUser(models.Model):
    telegram_user_id = models.CharField(max_length=18)
    current_service = models.ForeignKey('XrayServer', models.SET_NULL, 'server_users', null=True, blank=True)


class XrayServer(models.Model):
    country = models.CharField(max_length=128, unique=True)
    capacity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)


class XrayPort(models.Model):
    port_number = models.PositiveIntegerField()
    server = models.ForeignKey(XrayServer, models.CASCADE, 'ports')
    user = models.ForeignKey(XrayUser, models.CASCADE, 'ports')


