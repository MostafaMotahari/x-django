from django.conf import settings

from pyrogram import Client
from pyrogram import filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

from x_profile import models

@Client.on_message(filters.private & filters.command('start'))
def start(client, message, started=True):
    user, is_created = models.XrayUser.objects.get_or_create(telegram_user_id=message.from_user.id, 
                                        defaults={'username': message.from_user.username})
    try:
        is_channel_memeber = True if client.get_chat_member(settings.MAIN_TELEGRAM_CHANNEL, message.from_user.id) else False
    except UserNotParticipant:
        is_channel_memeber = False

    if is_channel_memeber:
        if started:
            message.reply_text(
                'Welcome to XDjango bot.\n'
                'You can get free V2ray connection here.\n\n'
                'To get your V2ray connection, click on the **Free V2ray** button.',
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [KeyboardButton('Free V2ray')],
                    ],
                    resize_keyboard=True
                )
            )
        else:
            return True

    else:
        message.reply_text(
            'You must join our channel to use services of this bot.'
            'So please join to below channel and restart the bot.',
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('Join Us ...', url='https://t.me/' + settings.MAIN_TELEGRAM_CHANNEL),],
                ]
            )
        )
        return False
