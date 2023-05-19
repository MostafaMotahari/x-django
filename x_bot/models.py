from django.db import models

# Create your models here.
class XrayUser(models.Model):
    telegram_user_id = models.CharField(max_length=18)
    donated_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.telegram_user_id


class XrayServer(models.Model):
    country = models.CharField(max_length=128, unique=True)
    capacity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    sni = models.CharField(max_length=32)
    domain = models.CharField(max_length=32, default='localhost')
    xui_port = models.IntegerField()
    xui_username = models.CharField(max_length=32)
    xui_password = models.CharField(max_length=32)

    def __str__(self):
        return self.country

    @property
    def xui_api_url(self):
        return 'http://' + self.domain + ':' + str(self.xui_port) + '/panel/api/'

    @property
    def xui_root_url(self):
        return 'http://' + self.domain + ':' + str(self.xui_port)


class XrayService(models.Model):
    user = models.ForeignKey(XrayUser, models.CASCADE, 'current_services')
    server = models.ForeignKey(XrayServer, models.SET_NULL, 'services', null=True, blank=True)
    uuid = models.CharField(max_length=32, unique=True)
    short_uuid = models.CharField(max_length=32, unique=True)
    inbound_id = models.IntegerField()
    price = models.IntegerField(default=0)
    connection_code = models.CharField(max_length=526)
    connection_qr = models.CharField(max_length=128)


    def __str__(self):
        return self.user.telegram_user_id + '-' + self.server.country


class XrayPort(models.Model):
    port_number = models.PositiveIntegerField()
    server = models.ForeignKey(XrayServer, models.CASCADE, 'ports')
    user = models.ForeignKey(XrayUser, models.CASCADE, 'ports')
