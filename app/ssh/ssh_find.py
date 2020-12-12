import os
from dotenv import load_dotenv
import paramiko
import time
import io

load_dotenv()
remote_user = 'postgres'
remote_host = 'pi0'
remote_port = 22
ssh_key = os.getenv("ssh_key")
  
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(remote_host, port=remote_port, username=remote_user, key_filename=ssh_key)
transport = client.get_transport()
channel = client.invoke_shell()


def sf_lucky():
    stdin = channel.makefile('w')
    stdout = channel.makefile('r')
    stdin.write('''
    cd /opt/ls-cluster-v0.0.1/models
    python3 -c 'import main; x = main.find_lucky(); print(x)'
    exit
    ''')

    while True:
        line = stdout.readline()
        if not line:
            break
        if line.strip().startswith('County'):
            print(line.rstrip())
        elif line.strip().startswith('0  '):
            print(line.rstrip())

    stdout.close()
    stdin.close()
    client.close()
