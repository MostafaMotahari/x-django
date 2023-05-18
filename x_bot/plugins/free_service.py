from pyrogram import Client
from pyrogram import filters
from django.conf import settings
import json
import requests
import shortuuid

from x_bot.plugins import functions
from x_bot import models
 

@Client.on_callback_query(filters.regex("^free_(.*)$"))
def free_v2ray(client, callback_query):
    user = models.XrayUser.objects.get(telegram_user_id=callback_query.from_user.id)
    server = models.XrayServer.objects.get(country=callback_query.data.split("_")[-1])

    try:
        current_service = models.XrayService.objects.get(user=user, price=0)
        client.send_message(callback_query.message.chat.id, 'You currently have a free service!')
        return False

    except models.XrayService.DoesNotExist:
        pass

    login = requests.request("POST", server.xui_root_url + '/login', headers={}, data={
        "username": server.xui_username,
        "password": server.xui_password
    })

    remark = str(callback_query.from_user.id) + '-' + server.country
    uuid, short_uuid = functions.get_uuid()
    pub_key, pri_key = functions.get_keys()
    port = functions.get_port()

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
        "streamSettings": functions.get_stream_settings(pub_key, pri_key, short_uuid, server.sni),
        "sniffing": json.dumps({
            "enabled": True,
            "destOverride": ["http","tls","quic"]
        })
    }
    headers = {'Accept': 'application/json'}

    response = requests.request("POST", server.xui_api_url + 'inbounds/add',
                                headers=headers, data=payload, cookies=login.cookies)
    inbound_json = response.json()

    if inbound_json['success']:
        client_payload = {
            'id': inbound_json['obj']['id'],
            'settings': functions.get_client(remark, uuid)
        }

        response = requests.request("POST", server.xui_api_url + 'inbounds/addClient',
                                    headers=headers, data=client_payload, cookies=login.cookies)
        json_response = response.json()

        if json_response['success']:
            conn_str = f"{payload['protocol']}://{uuid}@{server.domain}:{port}?type=tcp&security=reality&fp=firefox&pbk={pub_key}&sni={server.sni}&flow=xtls-rprx-vision&sid={short_uuid}&spx=%2F#{remark}-{remark + '-Email'}"
            image_path = functions.make_qr_image(conn_str, remark)

            models.XrayService.objects.create(
                    user=user, connection_code=conn_str, connection_qr=image_path,
                    server=server, uuid=uuid, short_uuid=short_uuid)

            models.XrayPort.objects.create(user=user, server=server, port_number=port)

            client.send_photo(callback_query.message.chat.id, image_path, conn_str)
            return True
        
    client.send_message(callback_query.message.chat.id, 'Can not create a v2ray inbound for you!')
