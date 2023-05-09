from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from x_bot import models
from x_bot.filters.custom_filters import force_join_filter


@Client.on_message(filters.private & filters.regex("^Free V2ray$") & force_join_filter)
def get_servers(client, message):
    keyboard = []
    for server in models.XrayServer.objects.filter(is_active=True):
        keyboard.append([InlineKeyboardButton(server.country, callback_data=f'free_{server.country}')])

    message.reply_text(
        'Choose a server ...',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
