import subprocess
import qrcode

def get_uuid():
    result = subprocess.run(['xray', 'uuid'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()

def get_keys():
    result = subprocess.run(['xray', 'x25519'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    key_lines = result.split('\n')
    public_key = key_lines[0].split(":")[1].strip()
    private_key = key_lines[1].split(":")[1].strip()

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
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save(f"qr_codes/{file_name}.png")
    return f"qr_codes/{file_name}.png"
