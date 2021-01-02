import os
from dotenv import load_dotenv
import paramiko
import io
from ssh.connect import ssh_postgres as sshp
import main

def se_est_params(mode, pop, rad, fips):
    if mode == 'cluster':
        try:
            version, transport, channel, stdin, stdout = sshp()

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
            channel.close()
        except Exception as e:
            print('LAN cluster not found! Running locally. Error: %s' % e)
            main.params_estimate(pop, rad, fips)

def se_est_comps(mode, comps, fips):
    if mode == 'cluster':
        try:    
            version, transport, channel, stdin, stdout = sshp()
            
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
            channel.close()
        except Exception as e:
            print('LAN cluster not found! Running locally. Error: %s' % e)
            main.comps_estimate(comps, fips)
