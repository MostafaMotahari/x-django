from pyrogram import Client
from pyrogram import filters

from x_profile import models
from x_profile import schema
from x_bot.filters.custom_filters import force_join_filter


@Client.on_message(filters.private & filters.regex("^Free V2ray$") & force_join_filter)
def free_v2ray(client, message):
    user = models.XrayUser.objects.get(telegram_user_id=message.from_user.id)
    inbound_setting = schema.INBOUND_SETTINGS.format()
    stream_setting = schema.STREAM_SETTINGS.format()
    sniffing_setting = schema.SNIFFING_SETTINGS.format()

    inbound = models.Inbounds(
        user_id = message.from_user.id,
        remark = str(message.from_user.id) + 
    )
