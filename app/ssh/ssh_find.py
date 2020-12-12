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
  



def sf_lucky():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(remote_host, port=remote_port, username=remote_user, key_filename=ssh_key)
    transport = client.get_transport()
    channel = client.invoke_shell()

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

def sf_state(state):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(remote_host, port=remote_port, username=remote_user, key_filename=ssh_key)
    transport = client.get_transport()
    channel = client.invoke_shell()

    stdin = channel.makefile('w')
    stdout = channel.makefile('r')
    stdin.write("""
    cd /opt/ls-cluster-v0.0.1/models
    python3 -c 'import main; x = main.find_state("%s"); print(x)'
    exit
    """ % state)

    while True:
        line = stdout.readline()
        # print(line.rstrip())
        if not line:
            break
        elif line.strip().startswith('County'):
            print(line.rstrip())
        else: 
            try:
                if line.strip()[0].isdigit():
                    if line.strip()[1:3].isspace():
                        print(line.rstrip())
            except IndexError:
                pass
        # elif line.strip().startswith('0  '):
        #     print(line.rstrip()[0])
        #     print(line.rstrip()[1:2])
        

    stdout.close()
    stdin.close()
    client.close()
