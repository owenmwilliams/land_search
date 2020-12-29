import os
from dotenv import load_dotenv
import paramiko
import io
from connect import ssh_postgres as sshp

# TODO: Check that sshp function works here, then apply to all others

def se_est_params(pop, rad, fips):
    transport, channel = sshp()
    stdin = channel.makefile('w')
    stdout = channel.makefile('r')
    stdin.write("""
    cd /opt/ls-cluster-{0}/models
    python3 -c 'import main; x = main.params_estimate({1}, {2}, {3}); print(x)'
    exit
    """.format(version, pop, rad, fips))

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

def se_est_comps(comps, fips):
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
    python3 -c 'import main; x = main.comps_estimate({1}, {2}); print(x)'
    exit
    """.format(version, comps, fips))

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
