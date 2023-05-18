from django.db import models

# Create your models here.
class XrayUser(models.Model):
    telegram_user_id = models.CharField(max_length=18)


class XrayServer(models.Model):
    country = models.CharField(max_length=128, unique=True)
    capacity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)


class XrayService(models.Model):
    user = models.ForeignKey(XrayUser, models.CASCADE, 'current_services')
    server = models.OneToOneField(XrayServer, models.SET_NULL, null=True, blank=Ture)
    price = models.IntegerField(default=0)
    connection_code = models.CharField(max_length=526)
    connection_qr = models.CharField(max_length=128)

class XrayPort(models.Model):
    port_number = models.PositiveIntegerField()
    server = models.ForeignKey(XrayServer, models.CASCADE, 'ports')
    user = models.ForeignKey(XrayUser, models.CASCADE, 'ports')


