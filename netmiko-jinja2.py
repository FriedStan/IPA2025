from netmiko import ConnectHandler
import yaml
from jinja2 import Environment, FileSystemLoader

with open("config.yaml") as f:
    config = yaml.safe_load(f)

USERNAME = config["credentials"]["username"]
PRIVATE_KEY = config["credentials"]["private_key"]
DEVICES = config["devices"]

env = Environment(loader=FileSystemLoader("templates"))

device_params = {
    'device_type': 'cisco_ios',
    'ip': None,
    'username': USERNAME,
    'use_keys': True,
    'key_file': PRIVATE_KEY,
    'disabled_algorithms': {
        'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512'],
    }
}

def connect_to(device_name):
    temp_params = device_params.copy()
    temp_params["ip"] = DEVICES.get(device_name).get("ip")
    return temp_params

def render_template(template_name, context):
    template = env.get_template(template_name)
    rendered_config = template.render(context)
    commands = rendered_config.strip().splitlines()
    return commands

for name in DEVICES:
    with ConnectHandler(**connect_to(name)) as ssh:
        is_r2 = False
        if(name == "S1"):
            print("--- Currently configure S1 ---")
            print("--- @[Vlan101] ---")
            ssh.send_config_set(render_template("S_config.j2", {}))
        elif(name == "R1"):
            print("--- Currently configure R1 ---")
            print("--- @[OSPF] ---")
            ssh.send_config_set(render_template("R_config.j2", {
                "ospf_networks": [
                    "192.168.120.0 0.0.0.255",
                    "192.168.121.0 0.0.0.255"
                ],
                "R2": is_r2
                }))
        elif(name == "R2"):
            is_r2 = True
            print("--- Currently configure R2 ---")
            print("--- @[OSPF] and [NAT/PAT] ---")
            ssh.send_config_set(render_template("R_config.j2", {
                "ospf_networks": [
                    "192.168.123.0 0.0.0.255",
                    "192.168.121.0 0.0.0.255"
                ],
                "R2": is_r2
                }))
        else:
            pass
        ssh.send_config_set(render_template("management_restrict_config.j2", {}))