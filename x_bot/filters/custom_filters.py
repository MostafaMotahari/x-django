from pyrogram import filters
from x_bot.plugins.start import start

force_join_filter = filters.create(lambda _, __, msg: start(__, msg, False))
