from pyrogram import Client
from pyrogram import filters
import json

from x_profile import models as profile_models
from x_profile import schema
from x_bot.filters.custom_filters import force_join_filter


@Client.on_callback_query(filters.regex("^free_(.*)$"))
def free_v2ray(client, callback_query):
    remark = str(callback_query.from_user.id) + callback_query.data.split("_")[-1]
    stream_setting = schema.STREAM_SETTINGS
    sniffing_setting = schema.SNIFFING_SETTINGS
    inbound_setting = schema.INBOUND_SETTINGS
    inbound_setting['id'] = "12"
    inbound_setting['tagId'] = remark

    inbound = profile_models.Inbounds.objects.create(
        user_id = callback_query.from_user.id,
        remark = remark,
        port=int(str(callback_query.from_user.id)[-1:-4]),
        protocol='vmess',
        settings=json.dumps(inbound_setting),
        stream_settings=json.dumps(stream_setting),
        tag='inbound' + str(callback_query.from_user.id),
        sniffing=json.dumps(sniffing_setting)
    )

    client.send_message(callback_query.chat.id, 'Created')
