import platform
import os
import netifaces
import requests
import json

def GetBasicInformation(uuid):
    windows_info = {}
    ip_addresses = {}
    mac_addresses = {}

    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            ip_addresses.setdefault('IPv4', []).append(addresses[netifaces.AF_INET][0]['addr'])
        if netifaces.AF_INET6 in addresses:
            ip_addresses.setdefault('IPv6', []).append(addresses[netifaces.AF_INET6][0]['addr'])

    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_LINK in addresses:
            mac_addresses[interface] = addresses[netifaces.AF_LINK][0]['addr']

    windows_info['Operation System'] = platform.system()
    windows_info['Computer Name'] = os.environ['COMPUTERNAME']
    windows_info['IP Adresses'] = json.dumps(ip_addresses)
    windows_info['Mac Adresses'] = json.dumps(mac_addresses)
    windows_info['uuid'] = uuid
    
    return windows_info

basicinformation = GetBasicInformation("312cfe03-869a-45db-91e0-84bbdfde2260")
api_url = "http://localhost:5000/api/getbasicinformation"
response_api = requests.post(api_url,  json=basicinformation)


