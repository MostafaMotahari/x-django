from pyrogram.client import Client
from decouple import config

PLUGINS = dict(root='x_bot/plugins')

app = Client(
    "XDBot",
    api_id=config("API_ID"),
    api_hash=config("API_HASH"),
    bot_token=config("BOT_TOKEN"),
    plugins=PLUGINS,
)
