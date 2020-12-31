import os
from dotenv import load_dotenv
import paramiko
import io
from ssh.connect import ssh_postgres as sshp
import main

# TODO: Update to call main.assess function on cluster or local...doc path should be cluster or local?

def sa_assess(doc_path):
    if mode == 'cluster':
        try:
            version, transport, channel, stdin, stdout = sshp()

            stdin.write("""
            cd /opt/ls-cluster-{0}/models
            python3 -c 'import main; x = main.assess({1}); print(x)'
            exit
            """.format(version, doc_path))

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
            main.params_estimate(doc_path)
    else:
        main.assess(doc_path)
