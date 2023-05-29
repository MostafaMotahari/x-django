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
        callback_query.message.edit_text('You currently have a free service!')
        return False

    except models.XrayService.DoesNotExist:
        pass

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
                    server=server, uuid=uuid, short_uuid=short_uuid, inbound_id=inbound_json['obj']['id'])

            models.XrayPort.objects.create(user=user, server=server, port_number=port)

            client.send_photo(callback_query.message.chat.id, image_path, conn_str)
            return True
        
    callback_query.message.edit_text('Can not create a v2ray inbound for you!')
