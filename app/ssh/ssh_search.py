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
version = os.getenv("version")

def ss_search_simple(value, share, pop):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(remote_host, port=remote_port, username=remote_user, key_filename=ssh_key)
    transport = client.get_transport()
    channel = client.invoke_shell()

    stdin = channel.makefile('w')
    stdout = channel.makefile('r')
    stdin.write("""
    cd /opt/ls-cluster-{0}/models
    python3 -c 'import main; x = main.search_all({1}, {2}, {3}); print(x)'
    exit
    """.format(version, value, share, pop))

    while True:
        line = stdout.readline()
        if not line:
            break
        elif line.strip().startswith('*****'):
            while not line.strip().startswith('#####'):
                line = stdout.readline()
                print(line.rstrip())
            print('_________________________________________________________')

    stdout.close()
    stdin.close()
    client.close()

def ss_search_complex(value, share, pop, air_prox, parks_prox, parks_num):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(remote_host, port=remote_port, username=remote_user, key_filename=ssh_key)
    transport = client.get_transport()
    channel = client.invoke_shell()

    stdin = channel.makefile('w')
    stdout = channel.makefile('r')
    stdin.write("""
    cd /opt/ls-cluster-{0}/models
    python3 -c 'import main; x = main.search_complex({1}, {2}, {3}, {4}, {5}, {6}); print(x)'
    exit
    """.format(version, value, share, pop, air_prox, parks_prox, parks_num))
    
    while True:
        line = stdout.readline()
        if not line:
            break
        elif line.strip().startswith('*****'):
            while not line.strip().startswith('#####'):
                line = stdout.readline()
                print(line.rstrip())
            print('_________________________________________________________')

    stdout.close()
    stdin.close()
    client.close()