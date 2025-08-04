from netmiko import ConnectHandler
import time


devices = {
    "R0": "172.31.106.1",
    "R1": "172.31.106.4",
    "R2": "172.31.106.5",
    "S0": "172.31.106.2",
    "S1": "172.31.106.3"
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

def generate_descriptions(parsed_neighbors):
    descriptions = {}

    for n in parsed_neighbors:
        local_int = n["local_interface"]
        neighbor = n["neighbor_name"]
        remote_int = f"{n['platform']} {n['neighbor_interface']}".strip()
        caps = n.get("capabilities", "").upper()

        if "H" in caps:
            desc = "Connect to PC"
        elif "R" in caps or "S" in caps:
            desc = f"Connect to {remote_int} of {neighbor.split('.')[0]}"
        else:
            desc = f"Connect to {neighbor}"

        descriptions[local_int] = desc

    return descriptions

def connect_to(device_name):
    temp_params = device_params.copy()
    temp_params["ip"] = devices[device_name]
    return temp_params

def choose_device(name):
    with ConnectHandler(**connect_to(name)) as ssh:
        output = ssh.send_command("show cdp neighbor", use_textfsm=True)
        interface_descriptions = generate_descriptions(output)
        if(name == "R1"):
            interface_descriptions["Gig 0/1"] = "Connect to PC"
        elif(name == "R2"):
            interface_descriptions["Gig 0/3"] = "Connect to WAN"
        elif(name == "S1"):
            interface_descriptions["Gig 1/1"] = "Connect to PC"
        print(f"--- @ {name} ---")
        for intf, desc in interface_descriptions.items():
                print(f"interface {intf}  -->  {desc}")
        return interface_descriptions

if __name__ == "__main__":
    for name in devices:
        choose_device(name)