from x_bot import models
from django import forms
from x_bot.plugins import functions
import requests
import json


class XrayInboundAdminForm(forms.ModelForm):
    class Meta:
        model = models.XrayInbound
        fields = ('__all__')

    def create(self, login_cookies, *args, **kwargs):
        uuid, short_uuid = functions.get_uuid()
        pub_key, pri_key = functions.get_keys()
        port = functions.get_port()

        payload = {
            "enable": True,
            "remark": self.cleaned_data['remark'],
            "listen": '',
            "port": port,
            "protocol": self.cleaned_data['protocol'],
            "expiryTime": 0,
            "settings": json.dumps({
                "clients": [],
                "decryption": "none",
                "fallbacks": []
            }),
            "streamSettings": functions.get_stream_settings(pub_key, pri_key, short_uuid, self.cleaned_data['sni']),
            "sniffing": json.dumps({
                "enabled": True,
                "destOverride": ["http","tls","quic"]
            })
        }
        headers = {'Accept': 'application/json'}

        response = requests.request("POST", self.cleaned_data['server'].xui_api_url + 'inbounds/add',
                                    headers=headers, data=payload, cookies=login_cookies)
        inbound_json = response.json()

        if inbound_json['success']:
            self.cleaned_data['short_uuid'] = short_uuid
            self.cleaned_data['private_key'], self.cleaned_data['public_key'] = pri_key, pub_key
            self.cleaned_data['inbound_id'] = inbound_json['obj']['id']
            self.cleaned_data['port'] = models.XrayPort.objects.create(port_number=port)

            super(XrayInboundAdminForm, self).save(commit=True)
            return True
        return False

    def clean(self):
        if login_cookies := functions.get_login_cookie(self.cleaned_data['server']):
            if self.create(login_cookies):
                return self.cleaned_data
        raise forms.ValidationError('Cant connect to x-ui api server!')


