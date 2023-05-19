from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

from x_bot import models
from x_bot.filters.custom_filters import force_join_filter


@Client.on_message(filters.private & filters.regex("^Your stats$") & force_join_filter)
def user_stats(client, message):
    user = models.XrayUser.objects.get(telegram_user_id=message.from_user.id)

    keyboard = []
    for service in user.current_services.all():
        keyboard.append([InlineKeyboardButton(
            service.server.country + ' ' + str(service.price) + '$',
            callback_data=f'get_stats_{service.pk}'
        )])

    message.reply_text(
        f"Hey! {message.from_user.first_name}\n"
        f"You donaited {user.donated_amount} to us!\n\n"
        "Your current services are showing below.\n"
        "Tap the buttons to see your services stats:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


@Client.on_callback_query(filters.regex("^get_stats_(.*)$"))
def service_stats(client, callback_query):
    service = models.XrayService.objects.get(pk=callback_query.data.split("_")[-1])

    login = requests.request("POST", service.server.xui_root_url + '/login', headers={}, data={
        "username": service.server.xui_username,
        "password": service.server.xui_password
    })

    headers = {'Accept': 'application/json'}
    response = requests.request("GET", service.server.xui_api_url + f'inbounds/get/{service.inbound_id}',
                                headers=headers, cookies=login.cookies)
    inbound_json = response.json()

    if inbound_json['success']:
        client.message.reply_text(
            f"Server name: {service.server.country}\n"
            f"Price: {service.price} USD\n"
            f"Download: {inbound_json['obj']['down']}\n"
            f"Upload: {inbound_json['obj']['up']}\n"
            f"Usage: {inbound_json['obj']['total']}\n",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Get credentials", callback_data=f"get_credentials_{service.pk}")],
                    [InlineKeyboardButton("Back to stats")],
                ]
            )
        )
        return True

    client.send_message(callback_query.message.chat.id, 'Can not get stats. please try again later.')


@Client.on_callback_query(filters.regex("^get_credentials_(.*)$"))
def get_service_credentails(client, callback_query):
    service = models.XrayService.objects.get(pk=callback_query.data.split("_")[-1])

    client.send_photo(
        callback_query.message.chat.id,
        service.connection_qr,
        service.connection_code
    )
