import ipaddress

def validate_ip(address):
    try:
        ipaddress.IPv4Address(address)
        return True
    except ValueError:
        return False

def validate_mask(mask):
    try:
        ip = ipaddress.IPv4Network(f"0.0.0.0/{mask}", strict=False)
        return str(ip.netmask) == mask
    except ValueError:
        return False

def validate_port(port: str) -> bool:
    if len(port) == 0:
        return False
    if int(port) < 0 or int(port) > 65535:
        return False
    return True

def validate_string(string: str) -> bool:
    if len(string) == 0:
        return False
    return True

def validate_username(username: str) -> bool:
    return validate_string(username)

def validate_password(password: str) -> bool:
    return validate_string(password)
