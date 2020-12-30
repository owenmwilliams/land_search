import os
from dotenv import load_dotenv
import paramiko
import time
import io
import main
from ssh.connect import ssh_postgres as sshp

def sf_lucky(mode):
    if mode == 'cluster':
        try:
            version, transport, channel, stdin, stdout = sshp()

            stdin.write("""
            cd /opt/ls-cluster-{0}/models
            python3 -c 'import main; x = main.find_lucky(); print(x)'
            exit
            """.format(version))

            while True:
                line = stdout.readline()
                if not line:
                    break
                if line.strip().startswith('County'):
                    print(line.rstrip())
                elif line.strip().startswith('0  '):
                    print(line.rstrip())

            print('*********************************************************')
            stdout.close()
            stdin.close()
            client.close()
        except:
            print('LAN cluster not found! Running locally.')
            main.find_lucky()
    else:
        main.find_lucky()

def sf_state(mode, state):
    if mode == 'cluster':
        try:
            version, transport, channel, stdin, stdout = sshp()

            stdin.write("""
            cd /opt/ls-cluster-{0}/models
            python3 -c 'import main; x = main.find_state("{1}"); print(x)'
            exit
            """.format(version, state))

            while True:
                line = stdout.readline()
                if not line:
                    break
                elif line.strip().startswith('County'):
                    print(line.rstrip())
                else: 
                    try:
                        if line.strip()[0:3].isdigit():
                            if line.strip()[3:5].isspace():
                                print(line.rstrip())
                        elif line.strip()[0:2].isdigit():
                            if line.strip()[2:4].isspace():
                                print(line.rstrip())
                        elif line.strip()[0].isdigit():
                            if line.strip()[1:3].isspace():
                                print(line.rstrip())
                    except IndexError:
                        pass
            print('*********************************************************')
            stdout.close()
            stdin.close()
            client.close()
        except:
            print('LAN cluster not found! Running locally.')
            main.find_state(state)
    else:
        main.find_state(state)
