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

    service = models.XrayService(user=user)
    if service.save(server.inbounds.first()):
        client.send_photo(callback_query.message.chat.id, service.image_path, service.conn_str)
        return True
    callback_query.message.edit_text('Can not create a v2ray inbound for you!')
