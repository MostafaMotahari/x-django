from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class XrayUser(AbstractUser):
    telegram_user_id = models.CharField(max_length=18)
    current_service = models.ForeignKey('XrayServer', models.SET_NULL, 'server_users', null=True, blank=True)
    inbound = models.OneToOneField('Inbounds', models.SET_NULL, null=True, blank=True)


class XrayServer(models.Model):
    country = models.CharField(max_length=128)
    capacity = models.PositiveIntegerField(default=0)


class XrayPort(models.Model):
    port_number = models.PositiveIntegerField()
    server = models.ForeignKey(XrayServer, models.CASCADE, 'ports')
    user = models.ForeignKey(XrayUser, models.CASCADE, 'ports')
    inbound = models.OneToOneField('Inbounds', models.CASCADE)


class Inbounds(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    remark = models.TextField()
    enable = models.BooleanField(default=True)
    expiry_time = models.IntegerField()
    listen = models.TextField()
    port = models.IntegerField(unique=True)
    protocol = models.TextField()
    settings = models.TextField()
    stream_settings = models.TextField()
    tag = models.TextField(unique=True)
    sniffing = models.TextField()

    class Meta:
        db_table = 'inbounds'
