from pyrogram import Client
from pyrogram import filters
from django.conf import settings
import json
import requests
import random

from x_bot.plugins.functions import get_uuid, get_keys, make_qr_image
from x_bot import models
 

@Client.on_callback_query(filters.regex("^free_(.*)$"))
def free_v2ray(client, callback_query):
    user = models.XrayUser.objects.get(telegram_user_id=callback_query.from_user.id)

    try:
        current_service = models.XrayService.objects.get(user=user, price=0)
        client.send_message(callback_query.message.chat.id, 'You currently have a free service!')
        return False

    except models.XrayService.DoesNotExist:
        pass

    login = requests.request("POST", settings.XUI_URL + '/login', headers={}, data={
        "username": settings.XUI_USER,
        "password": settings.XUI_PASS
    })

    server = models.XrayServer.objects.get(country=callback_query.data.split("_")[-1])
    remark = str(callback_query.from_user.id) + '-' + server.country
    pub_key, pri_key = get_keys()
    stream_settings = {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
            "show": False,
            "xver": 0,
            "dest": "yahoo.com:443",
            "serverNames": ["yahoo.com", "www.yahoo.com"],
            "privateKey": pri_key,
            "minClient": "",
            "maxClient": "",
            "maxTimediff": 0,
            "shortIds": [],
            "settings": {
                "publicKey": pub_key,
                "fingerprint": "firefox",
                "serverName": ""
            }
        },
        "tcpSettings": {
            "acceptProxyProtocol": False,
            "header": {"type": "none"}
        }
    }

    port = None
    for port in range(10000, 12000):
        try:
            models.XrayPort.objects.get(port_number=port)
            continue
        except models.XrayPort.DoesNotExist:
            port = port
            break

    payload = {
        "enable": True,
        "remark": remark,
        "listen": '',
        "port": port,
        "protocol": "vless",
        "expiryTime": 0,
        "settings": json.dumps({
            "clients": [],
            "decryption": "none",
            "fallbacks": []
        }),
        "streamSettings": json.dumps(stream_settings),
        "sniffing": json.dumps({
            "enabled": True,
            "destOverride": ["http","tls","quic"]
        })
    }
    headers = {'Accept': 'application/json'}

    response = requests.request("POST", settings.XUI_API_URL + 'inbounds/add',
                                headers=headers, data=payload, cookies=login.cookies)
    inbound_json = response.json()

    if inbound_json['success']:
        uuid = get_uuid()
        v2ray_settings = {
            "clients":[{
                "id": uuid,
                "alterId": 0,
                "email": remark + "-Email",
                "limitIp": 2,
                "totalGB": 10,
                "expiryTime": 1682864675944,
                "enable": True,
                "tgId": "",
                "subId": ""
            }]
        }

        client_payload = {
            'id': inbound_json['obj']['id'],
            'settings': json.dumps(v2ray_settings)
        }

        response = requests.request("POST", settings.XUI_API_URL + 'inbounds/addClient',
                                    headers=headers, data=client_payload, cookies=login.cookies)
        json_response = response.json()

        if json_response['success']:
            conn_str = f"vless://{uuid}@{settings.REGISTERED_DOMAIN}:{payload['port']}?type=tcp&security=reality&fp={stream_settings['realitySettings']['settings']['fingerprint']}&pbk={pub_key}&sni={stream_settings['realitySettings']['serverNames'][0]}#{remark}-{remark + '-Email'}"
            image_path = make_qr_image(conn_str, remark)

            models.XrayService.objects.create(user=user, connection_code=conn_str, connection_qr=image_path, server=server)

            models.XrayPort.objects.create(user=user, server=server, port=port)

            client.send_photo(callback_query.message.chat.id, image_path, conn_str)
            return True
        
    client.send_message(callback_query.message.chat.id, 'Can not create a v2ray inbound for you!')
