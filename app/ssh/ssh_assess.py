import os
from dotenv import load_dotenv
import paramiko
import io
from ssh.connect import ssh_postgres as sshp
from ssh.connect import yaml_import as yaml
from ssh.connect import yaml_unpack
import main

def sa_assess(mode, doc_path):
    if mode == 'cluster':
        try:
            version, transport, channel, stdin, stdout = sshp()

            minimums, maximums, weights, radius = yaml(doc_path)
            pop_min, value_min, share_min, air_min, parks_min, pop_max, value_max, share_max, air_max, parks_max, pop_weight, value_weight, share_weight, air_weight, parks_weight, air_radius, parks_radius = yaml_unpack(minimums, maximums, weights, radius)

            stdin.write("""
            cd /opt/ls-cluster-{0}/models
            python3 -c 'import main; x = main.cluster_assess({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}); print(x)'
            exit
            """.format(version, pop_min, value_min, share_min, air_min, parks_min, pop_max, value_max, share_max, air_max, parks_max, pop_weight, value_weight, share_weight, air_weight, parks_weight, air_radius, parks_radius))

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
            minimums, maximums, weights, radius = yaml(doc_path)
            main.assess(minimums, maximums, weights, radius)
