def rm_http(address: str) -> str:
    return address.replace('http://', '').replace('https://', '')
