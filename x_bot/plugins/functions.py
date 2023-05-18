import subprocess
import qrcode
import shortuuid

from x_bot.models import XrayService

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
        short_uuid = shortuuid.uuid()
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
    public_key = key_lines[0].split(":")[1].strip()
    private_key = key_lines[1].split(":")[1].strip()

    return (public_key, private_key)

def make_qr_image(data: str, file_name: str):
#    qr = qrcode.QRCode(
#        version=1,
#        error_correction=qrcode.constants.ERROR_CORRECT_H,
#        box_size=10,
#        border=4,
#    )
    image = qrcode.make(data)
    # qr_image = qr.make_image(fill_color="black", back_color="white")
    image.save(f"qr_codes/{file_name}.png")
    return f"qr_codes/{file_name}.png"
