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

S1_vlan101_config = ["vlan 101",
                     "int vlan101",
                     "no shut",
                     "int g0/1",
                     "switchport access vlan 101",
                     "int g1/1",
                     "switchport access vlan 101"
                    ]

R1_ospf_config = [
    "router ospf 1 vrf control-data",
    "network 192.168.120.0 0.0.0.255 area 0",
    "network 192.168.121.0 0.0.0.255 area 0"
]

R2_ospf_config = [
    "router ospf 1 vrf control-data",
    "network 192.168.123.0 0.0.0.255 area 0",
    "network 192.168.121.0 0.0.0.255 area 0",
    "default-information originate"
]

R2_pat_config = [
    "int g0/2",
    "ip nat inside",
    "int g0/3",
    "ip nat outside",
    "ip access-list standard pat1",
    "permit 192.168.123.0 0.0.0.255 any",
    "ip nat inside source list pat1 int g0/3 vrf control-data match-in-vrf"
]

telnet_ssh_only_config = [
    "ip access-list standard management-ssh-telnet",
    "permit 172.31.106.0 0.0.0.255",
    "permit 10.30.6.0 0.0.0.255",
    "permit 172.16.197.0 0.0.0.255", # This is vmnet for playing
    "line vty 0 4",
    "transport input telnet ssh",
    "access-class management-ssh-telnet in"
]



def connect_to(device_name):
    temp_params = device_params.copy()
    temp_params["ip"] = devices[device_name]
    return temp_params

for name in devices:
    with ConnectHandler(**connect_to(name)) as ssh:
        if(name == "S1"):
            print("--- Currently configure S1 ---")
            print("--- Currently configure [Vlan101] ---")
            ssh.send_config_set(S1_vlan101_config)
        elif(name == "R1"):
            print("--- Currently configure R1 ---")
            print("--- @[OSPF] ---")
            ssh.send_config_set(R1_ospf_config)
        elif(name == "R2"):
            print("--- Currently configure R2 ---")
            print("--- @[OSPF] ---")
            ssh.send_config_set(R2_ospf_config)
            print("--- @[NAT/PAT] ---")
            ssh.send_config_set(R2_pat_config)
        else:
            pass

        print("--- @[Telnet/SSH Only] ---")
        ssh.send_config_set(telnet_ssh_only_config)
        print("\n")