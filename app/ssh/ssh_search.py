import os
from dotenv import load_dotenv
import paramiko
import time
import io
from ssh.connect import ssh_postgres as sshp
import main

load_dotenv()
remote_user = 'postgres'
remote_host = 'pi0'
remote_port = 22
ssh_key = os.getenv("ssh_key")
version = os.getenv("version")

def ss_search_simple(mode, value, share, pop):
    if mode == 'cluster':
        try:
            version, transport, channel, stdin, stdout = sshp()

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
            channel.close()
        except Exception as e:
            print('LAN cluster not found! Running locally. Error: %s' % e)
            main.search_all(value, share, pop)
    else:
        main.search_all(value, share, pop)

def ss_search_complex(mode, value, share, pop, air_prox, parks_prox, parks_num):
    if mode == 'cluster':
        try:
            version, transport, channel, stdin, stdout = sshp()
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
            channel.close()
        except Exception as e:
            print('LAN cluster not found! Running locally. Error: %s' % e)
            main.search_complex(value, share, pop, air_prox, parks_prox, parks_num)
    else:
        main.search_complex(value, share, pop, air_prox, parks_prox, parks_num)
                   