from django.db import models

# Create your models here.
class Inbound(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    remark = models.TextField()
    enable = models.BooleanField(default=True)
    expiry_time = models.IntegerField(default=0)
    listen = models.TextField(default="")
    port = models.IntegerField(unique=True)
    protocol = models.TextField()
    settings = models.TextField()
    stream_settings = models.TextField()
    tag = models.TextField(unique=True)
    sniffing = models.TextField()

    class Meta:
        db_table = 'inbounds'


class InboundClientIP(models.Model):
    id = models.AutoField(primary_key=True)
    client_email = models.TextField(unique=True)
    ips = models.TextField()

    class Meta:
        db_table = 'inbound_client_ips'


class ClientTraffics(models.Model):
    id = models.AutoField(primary_key=True)
    inbound = models.ForeignKey(Inbound, on_delete=models.CASCADE, related_name='client_traffics')
    enable = models.DecimalField(max_digits=1, decimal_places=0)
    email = models.TextField(unique=True)
    up = models.IntegerField()
    down = models.IntegerField()
    expiry_time = models.IntegerField()
    total = models.IntegerField()

    class Meta:
        db_table = 'client_traffics'


class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.TextField()
    value = models.TextField()

    class Meta:
        db_table = 'settings'


class AdminUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.TextField()
    password = models.TextField()
    login_secret = models.TextField()

    class Meta:
        db_table = 'users'


