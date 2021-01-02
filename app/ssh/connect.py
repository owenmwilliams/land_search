import os
from dotenv import load_dotenv
import paramiko
import yaml

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

def yaml_import(doc_path):
    stream = open(doc_path)
    boundaries = yaml.load_all(stream, Loader=yaml.FullLoader)
    for data in boundaries:
        for j, k in data.items():
            if j == 'minimums':
                minimums = k
            elif j == 'maximums':
                maximums = k
            elif j == 'weights':
                weights = k
            elif j == 'radius':
                radius = k
    return minimums, maximums, weights, radius

def yaml_unpack(minimums, maximums, weights, radius):
    pop_min, value_min, share_min, air_min, parks_min = minimums['pop'], minimums['value'], minimums['share'], minimums['air'], minimums['parks']
    pop_max, value_max, share_max, air_max, parks_max = maximums['pop'], maximums['value'], maximums['share'], maximums['air'], maximums['parks']
    pop_weight, value_weight, share_weight, air_weight, parks_weight = weights['pop'], weights['value'], weights['share'], weights['air'], weights['parks']
    air_radius, parks_radius = radius['air'], radius['parks']
    return pop_min, value_min, share_min, air_min, parks_min, pop_max, value_max, share_max, air_max, parks_max, pop_weight, value_weight, share_weight, air_weight, parks_weight, air_radius, parks_radius
