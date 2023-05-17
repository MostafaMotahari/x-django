import subprocess

def get_uuid():
    result = subprocess.run(['xray', 'uuid'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()

def get_keys():
    result = subprocess.run(['xray', 'x25519'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    key_lines = result.split('/n')
    public_key = key_lines[0].split(":")[1].strip()
    private_key = key_lines[1].split(":")[1].strip()

    return (public_key, private_key)
