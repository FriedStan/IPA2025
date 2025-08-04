from netmiko import ConnectHandler
import re

int_up_regex = r"(\S+\/\d is up.*is up)"

devices = {
    "R1": "172.31.106.4",
    "R2": "172.31.106.5",
}

device_params = {
    'device_type': 'cisco_ios',
    'ip': None,
    'username': 'admin',
    'use_keys': True,
    'key_file': '/home/kuqing/.ssh/ipa_rsa',
    'disabled_algorithms': {
        'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512'],
    }
}

def connect_to(device_name):
    temp_params = device_params.copy()
    temp_params["ip"] = devices[device_name]
    return temp_params

for name in devices:
    with ConnectHandler(**connect_to(name)) as ssh:
        text = ssh.send_command("show interface")
        active = re.findall(int_up_regex, text)
        print(f"--- Active interface(s) @ {name} ---")
        if(active):
            print(*active, sep="\n")
        else:
            print("None of the interface are active")
        print() 