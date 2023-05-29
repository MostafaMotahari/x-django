from django.db import models
import requests
from x_bot.plugins import functions
import json

# Create your models here.
class XrayUser(models.Model):
    telegram_user_id = models.CharField(max_length=18)
    donated_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.telegram_user_id


class XrayServer(models.Model):
    country = models.CharField(max_length=128, unique=True)
    domain = models.CharField(max_length=32, default='localhost')
    ssl_certificate = models.BooleanField(default=False)
    xui_port = models.IntegerField()
    xui_username = models.CharField(max_length=32)
    xui_password = models.CharField(max_length=32)

    def __str__(self):
        return self.country

    @property
    def xui_api_url(self):
        url_suffix = 'https://' if self.ssl_certificate else 'http://'
        return url_suffix + self.domain + ':' + str(self.xui_port) + '/panel/api/'

    @property
    def xui_root_url(self):
        url_suffix = 'https://' if self.ssl_certificate else 'http://'
        return url_suffix + self.domain + ':' + str(self.xui_port)


class XrayPort(models.Model):
    port_number = models.PositiveIntegerField()

    def __str__(self):
        return self.port_number


class XrayInbound(models.Model):
    class Protocol(models.TextChoices):
        VMESS = 'vmess', 'Vmess'
        VLESS = 'vless', 'Vless'
        TROJAN = 'trojan', 'Trojan'
        DOKODEMO = 'dokodemo', 'dokodemo'

    class Security(models.TextChoices):
        REALITY = 'reality', 'Reality' 
        TLS = 'tls', 'TLS'
        XTLS = 'xtls', 'XTLS'

    class UTLS(models.TextChoices):
        FIREFOX = 'firefox', 'Fire Fox'
        CHROME = 'chrome', 'Chrome'

    class Transmission(models.TextChoices):
        TCP = 'tcp', 'TCP'

    server = models.ForeignKey(XrayServer, models.CASCADE, 'inbounds')
    inbound_id = models.IntegerField(help_text='Dont fill this field! it will be filled automatically.')
    remark = models.CharField(max_length=36)
    protocol = models.CharField(max_length=8, choices=Protocol.choices)
    port = models.OneToOneField(XrayPort, models.PROTECT, related_name='inbound', help_text='Dont fill this field! it will be filled automatically.')
    total_flow = models.IntegerField(null=True, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    transmission = models.CharField(max_length=8, choices=Transmission.choices, default=Transmission.TCP)
    is_active = models.BooleanField(default=True)
    security = models.CharField(max_length=8, choices=Security.choices)
    sni = models.CharField(max_length=32)
    utls = models.CharField(max_length=8, choices=UTLS.choices)
    short_uuid = models.CharField(max_length=32, unique=True, help_text='Dont fill this field! it will be filled automatically.')
    private_key = models.CharField(max_length=46, help_text='Dont fill this field! it will be filled automatically.')
    public_key = models.CharField(max_length=46, help_text='Dont fill this field! it will be filled automatically.')

    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.protocol + ' - ' + self.security + ' - ' + self.utls

    def create(self, login_cookies, *args, **kwargs):
        uuid, short_uuid = functions.get_uuid()
        pub_key, pri_key = functions.get_keys()
        port = functions.get_port()

        payload = {
            "enable": True,
            "remark": self.remark,
            "listen": '',
            "port": port,
            "protocol": self.protocol,
            "expiryTime": 0,
            "settings": json.dumps({
                "clients": [],
                "decryption": "none",
                "fallbacks": []
            }),
            "streamSettings": functions.get_stream_settings(pub_key, pri_key, short_uuid, self.server.sni),
            "sniffing": json.dumps({
                "enabled": True,
                "destOverride": ["http","tls","quic"]
            })
        }
        headers = {'Accept': 'application/json'}

        response = requests.request("POST", self.server.xui_api_url + 'inbounds/add',
                                    headers=headers, data=payload, cookies=login_cookies)
        inbound_json = response.json()

        if inbound_json['success']:
            self.short_uuid = short_uuid
            self.private_key, self.public_key = pri_key, pub_key
            self.inbound_id = inbound_json['obj']['id']
            self.port = XrayPort.objects.create(port_number=port)

            super(XrayInbound, self).save(*args, **kwargs)
            return True
        return False

    def save(self, *args, **kwargs):
        if login_cookies := functions.get_login_cookie(self.server):
            self.create(login_cookies)
            return True
        return False


class XrayService(models.Model):
    user = models.ForeignKey(XrayUser, models.CASCADE, 'current_services')
    inbound = models.ForeignKey(XrayInbound, models.CASCADE, 'clients')
    uuid = models.CharField(max_length=32, unique=True)
    price = models.IntegerField(default=0)
    connection_code = models.CharField(max_length=526)
    connection_qr = models.CharField(max_length=128)

    def __str__(self):
        return self.user.telegram_user_id + '-' + self.server.country

    def save(self, *args, **kwargs):
        if not (login_cookies := functions.get_login_cookie(self.inbound.server)):
            return False

        uuid, short_uuid = functions.get_uuid()
        client_payload = {
            'id': self.inbound.inbound_id,
            'settings': functions.get_client(self.inbound.remark, uuid)
        }

        headers = {'Accept': 'application/json'}
        response = requests.request("POST", self.inbound.server.xui_api_url + 'inbounds/addClient',
                                    headers=headers, data=client_payload, cookies=login_cookies)
        json_response = response.json()

        if json_response['success']:
            self.conn_str = f"{self.inbound.protocol}://{uuid}@{self.inbound.server.domain}:{self.inbound.port}?type={self.inbound.transmission}&security={self.inbound.security}&fp={self.inbound.utls}&pbk={self.inbound.pub_key}&sni={self.inbound.server.sni}&flow=xtls-rprx-vision&sid={self.inbound.short_uuid}&spx=%2F#{self.inbound.remark}-{self.inbound.remark + '-Email'}"
            self.image_path = functions.make_qr_image(self.conn_str, self.inbound.remark)
            self.uuid = uuid
            super(XrayService, self).save(*args, **kwargs)
