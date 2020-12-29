import os
from dotenv import load_dotenv
import paramiko
import io
from ssh.connect import ssh_postgres as sshp
import main

# TODO: Check that sshp function works here, then apply to all others

def se_est_params(mode, pop, rad, fips):
    if mode == 'cluster':
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
    else:
        main.params_estimate(pop, rad, fips)

# TODO: Check to see if flag works here for local vs. cluster

def se_est_comps(mode, comps, fips):
    if mode == 'cluster':
        transport, channel = sshp()
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
    else:
        main.comps_estimate(comps, fips)
