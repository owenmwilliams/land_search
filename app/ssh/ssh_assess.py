import os
from dotenv import load_dotenv
import paramiko
import io
from ssh.connect import ssh_postgres as sshp
from ssh.connect import yaml_import as yaml
import main

def sa_assess(mode, doc_path):
    if mode == 'cluster':
        try:
            version, transport, channel, stdin, stdout = sshp()

            minimums, maximums, weights, radius = yaml(doc_path)

            stdin.write("""
            cd /opt/ls-cluster-{0}/models
            python3 -c 'import main; x = main.assess({1}, {2}, {3}, {4}); print(x)'
            exit
            """.format(version, minimums, maximums, weights, radius))

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
            main.assess(yaml(doc_path))
