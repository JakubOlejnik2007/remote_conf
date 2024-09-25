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
    if not string.isalnum():
        return False
    return True

def validate_username(username: str) -> bool:
    return validate_string(username)

def validate_password(password: str) -> bool:
    return validate_string(password)

def validate_hostname(hostname: str) -> bool:
    return validate_string(hostname) and len(hostname) <= 63

def validate_vlan_name(vlanName: str) -> bool:
    return validate_string(vlanName) and len(vlanName) <= 32

def validate_vlan_number(vlanNum: str) -> bool:
    return vlanNum.isdigit() and 0 < int(vlanNum) <= 4094