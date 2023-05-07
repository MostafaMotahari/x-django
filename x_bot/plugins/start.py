from pyrogram import Client
from pyrogram import filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

@Client.on_message(filters.private & filters.command('start'))
def start(client, message):
    message.reply_text(
        'Welcome to XDjango bot.\n'
        'You can get free V2ray connection here.\n\n'
        'To get your V2ray connection, click on the **Free V2ray** button.',
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton('Free V2ray')],
            ]
        )
    )
