import paramiko
import time
import os

devices = {
    "R0": "172.31.106.1",
    "R1": "172.31.106.4",
    "R2": "172.31.106.5",
    "S0": "172.31.106.2",
    "S1": "172.31.106.3"
}

private_key_path = os.path.expanduser("~/.ssh/ipa_rsa")
private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

paramiko.transport._preferred_kex = ("diffie-hellman-group14-sha1")
paramiko.transport._preferred_keys = ("ssh-rsa")

def backup_running_config(device_name, username="admin"):
    hostname = devices[device_name]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(
            hostname=hostname,
            username=username,
            pkey=private_key,
            look_for_keys=False,
            allow_agent=False,
            timeout=10
        )

        remote_conn = client.invoke_shell()
        time.sleep(1)
        remote_conn.send("terminal length 0\n")
        time.sleep(0.5)
        remote_conn.send("show running-config\n")
        time.sleep(2)

        output = remote_conn.recv(65535).decode('utf-8')

        file_path = f"./{device_name}_running_config.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output)

        print(f"[+] Saved running config for {device_name} -> {file_path}")

    except Exception as e:
        print(f"[!] Failed to backup {device_name} ({hostname}): {e}")
    finally:
        client.close()

def ssh_connect(device_name, username='admin'):
    hostname = devices[device_name]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=hostname,
            username=username,
            pkey=private_key,
            look_for_keys=False,
            allow_agent=False,
            timeout=10
        )

        stdin, stdout, stderr = client.exec_command("show version")
        print(f"\n=== {device_name} @ {hostname} ===")
        print(f"SUCCESS")

    except Exception as e:
        print(f"[!] Failed to connect to {hostname}: {e}")
    finally:
        client.close()

for name in devices:
  ssh_connect(name)
backup_running_config("R0")
