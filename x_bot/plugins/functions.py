import subprocess
import qrcode
import random
import json

from x_bot.models import XrayService, XrayPort

def get_uuid():
    while True:
        result = subprocess.run(['xray', 'uuid'], stdout=subprocess.PIPE)
        result = result.stdout.decode('utf-8').strip()
        try:
            XrayService.objects.get(uuid=result)
            continue
        except XrayService.DoesNotExist:
            break

    while True:
        short_uuid = ''.join(random.choices('0123456789abcdef', k=6))
        try:
            XrayService.objects.get(short_uuid=short_uuid)
            continue
        except XrayService.DoesNotExist:
            break

    return (result, short_uuid)

def get_keys():
    result = subprocess.run(['xray', 'x25519'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    key_lines = result.split('\n')
    private_key = key_lines[0].split(":")[1].strip()
    public_key = key_lines[1].split(":")[1].strip()

    return (public_key, private_key)

def make_qr_image(data: str, file_name: str):
    qr = qrcode.QRCode(
         version=1,
         error_correction=qrcode.constants.ERROR_CORRECT_H,
         box_size=10,
         border=4,
     )
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color=(24, 24, 24), back_color=(135, 88, 255))
    qr_image.save(f"qr_codes/{file_name}.png")

    return f"qr_codes/{file_name}.png"

def get_port():
    port = None
    for port in range(10000, 12000):
        try:
            XrayPort.objects.get(port_number=port)
            continue
        except XrayPort.DoesNotExist:
            return port

def get_stream_settings(pub_key, pri_key, short_uuid, server_name):
    stream_settings = {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
            "show": False,
            "xver": 0,
            "dest": server_name + ":443",
            "serverNames": [server_name, "www." + server_name],
            "privateKey": pri_key,
            "minClient": "",
            "maxClient": "",
            "maxTimediff": 0,
            "shortIds": [short_uuid],
            "settings": {
                "publicKey": pub_key,
                "fingerprint": "firefox",
                "serverName": "",
                "spiderX": "/"
            }
        },
        "tcpSettings": {
            "acceptProxyProtocol": False,
            "header": {"type": "none"}
        }
    }

    return json.dumps(stream_settings)

def get_client(remark, uuid, limit_ip=2, total_gb=20, expiry_time=1682864675944):
    client = {
        "clients":[{
            "id": uuid,
            "alterId": 0,
            "email": remark + "-Email",
            "limitIp": limit_ip,
            "totalGB": total_gb,
            "enable": True,
            "flow": "xtls-rprx-vision",
            "tgId": "",
            "subId": ""
        }]
    }

    return json.dumps(client)

def make_mono_str(text: str):
    return "```" + text + "```"
