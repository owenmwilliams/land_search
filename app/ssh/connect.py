import os
from dotenv import load_dotenv
import paramiko

def ssh_postgres():
    load_dotenv()
    ssh_key = os.getenv("ssh_key")
    version = os.getenv("version")
    remote_user = 'postgres'
    remote_host = 'pi0'
    remote_port = 22
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(remote_host, port=remote_port, username=remote_user, key_filename=ssh_key)
    transport = client.get_transport()
    channel = client.invoke_shell()
    stdin = channel.makefile('w')
    stdout = channel.makefile('r')
    return version, transport, channel, stdin, stdout
