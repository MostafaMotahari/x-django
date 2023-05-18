from pyrogram import Client
from pyrogram import filters
from django.conf import settings
import json
import requests

from x_bot.plugins.functions import get_uuid, get_keys
 

@Client.on_callback_query(filters.regex("^free_(.*)$"))
def free_v2ray(client, callback_query):
    login = requests.request("POST", settings.X_UI_URL + 'login', headers={}, data='username=mousiol&password=123')
    print(login.text)

    remark = str(callback_query.from_user.id) + '-' + callback_query.data.split("_")[-1]
    pub_key, pri_key = get_keys()
    stream_settings =  '{"network": "tcp", "security": "reality", "realitySettings": {"show": False, "xver": 0, "dest": "yahoo.com:443", "serverNames": ["yahoo.com", "www.yahoo.com"], "privateKey": "%s", "minClient": "", "maxClient": "", "maxTimediff": 0, "shortIds": [], "settings": {"publicKey": "%s", "fingerprint": "firefox", "serverName": ""}}, "tcpSettings": {"acceptProxyProtocol": False, "header": {"type": "none"}}}'

    payload = {
        'enable': True,
        'remark': remark,
        'listen': '',
        'port': 48965,
        'protocol': 'vless',
        'expiryTime': 0,
        'settings':
        '{"clients":[],"decryption":"none","fallbacks":[]}',
        'streamSettings': stream_settings % (pri_key, pub_key),
        'sniffing': '{"enabled":true,"destOverride":["http","tls","quic"]}'
    }
    headers = {
        'Accept': 'application/json'
    }
    print(payload)

    response = requests.request("POST", settings.X_UI_API_URL + 'inbounds/add', headers=headers, data=json.dumps(payload))
    json_response = response.json()
    print(json_response)

    if json_response['success']:
        uuid = get_uuid()
        v2ray_settings =  '{"clients":[{"id":"%s","alterId":0,"email":"%s","limitIp":2,"totalGB":10,"expiryTime":1682864675944,"enable":true,"tgId":"","subId":""}]}'

        payload = {
            'id': json_response['obj']['id'],
            'settings': v2ray_settings % (uuid, remark + " Email")
        }

        response = requests.request("POST", settings.X_UI_API_URL + 'inbounds/addClient', headers=headers, data=json.dumps(payload))

    client.send_message(callback_query.chat.id, 'Created')
